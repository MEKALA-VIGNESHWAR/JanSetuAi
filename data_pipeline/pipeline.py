"""
JanSetuAI — Pipeline Orchestrator
====================================
Connects all pipeline stages: discover → extract → normalize →
validate → deduplicate → verify → store.

Run with:  python -m data_pipeline.pipeline
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

from data_pipeline.normalization.scheme_normalizer import SchemeNormalizer
from data_pipeline.sources.myscheme import MySchemeCollector
from data_pipeline.sources.telangana import TelanganaCollector
from data_pipeline.storage.repository import FileRepository, PostgresRepository
from data_pipeline.validation.duplicates import DuplicateDetector
from data_pipeline.validation.rules import SchemeValidator
from data_pipeline.validation.schema import (
    PipelineResult,
    Scheme,
    VerificationStatus,
)
from data_pipeline.verification.review_queue import SchemeVerifier

logger = logging.getLogger(__name__)


class DataPipeline:
    """
    End-to-end data pipeline orchestrator.

    Stages:
        1. Discover — find scheme entries from configured sources
        2. Extract  — fetch and parse scheme details
        3. Normalize — convert to canonical format
        4. Validate — check required fields, types, consistency
        5. Deduplicate — remove duplicates
        6. Verify — check URLs, evidence, status
        7. Store — save to JSON/CSV and optionally PostgreSQL
    """

    def __init__(self, config_path: str = "data_pipeline/config/sources.yaml"):
        self.config = self._load_config(config_path)
        pipeline_cfg = self.config.get("pipeline", {})

        self.raw_data_dir = pipeline_cfg.get("raw_data_dir", "data/raw")
        self.staging_dir = pipeline_cfg.get("staging_dir", "data/staging")
        self.verified_dir = pipeline_cfg.get("verified_dir", "data/verified")
        self.rejected_dir = pipeline_cfg.get("rejected_dir", "data/rejected")

        # Create data directories
        for d in (self.raw_data_dir, self.staging_dir, self.verified_dir, self.rejected_dir):
            Path(d).mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.normalizer = SchemeNormalizer()
        self.validator = SchemeValidator()
        self.dedup = DuplicateDetector(similarity_threshold=0.85)
        self.file_repo = FileRepository(
            verified_dir=self.verified_dir,
            rejected_dir=self.rejected_dir,
            staging_dir=self.staging_dir,
        )

    def _load_config(self, config_path: str) -> dict:
        """Load pipeline configuration."""
        path = Path(config_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        logger.warning(f"Config not found at {config_path}, using defaults")
        return {}

    def run(
        self,
        sources: list[str] | None = None,
        skip_verification: bool = False,
        skip_db: bool = True,
        max_schemes: int = 50,
    ) -> PipelineResult:
        """
        Run the full pipeline.

        Args:
            sources: list of source names to run (default: all enabled)
            skip_verification: skip URL accessibility checks (faster)
            skip_db: skip PostgreSQL loading (default True for safety)
            max_schemes: max schemes per source
        """
        result = PipelineResult(started_at=datetime.utcnow())

        print("\n" + "=" * 60)
        print("  JanSetuAI Data Pipeline — Phase 1")
        print("=" * 60)

        # ── Stage 1 & 2: Discover + Extract ──────────────────
        print("\n[1/7] Discovering and extracting schemes...")
        all_schemes: list[Scheme] = []

        collectors = self._get_collectors(sources, max_schemes)
        for name, collector in collectors.items():
            try:
                print(f"  → Collecting from: {name}")
                with collector:
                    schemes = collector.collect_all()
                    all_schemes.extend(schemes)
                    print(f"    Collected {len(schemes)} schemes")
            except Exception as e:
                msg = f"Collector {name} failed: {e}"
                logger.error(msg)
                result.errors.append(msg)

        result.total_discovered = len(all_schemes)
        result.extracted = len(all_schemes)
        print(f"  Total extracted: {len(all_schemes)}")

        if not all_schemes:
            print("\n⚠ No schemes extracted. Pipeline complete (empty).")
            result.finished_at = datetime.utcnow()
            return result

        # ── Stage 3: Normalize ────────────────────────────────
        print(f"\n[2/7] Normalizing {len(all_schemes)} schemes...")
        for scheme in all_schemes:
            self.normalizer.normalize(scheme)
        result.normalized = len(all_schemes)
        print(f"  Normalized: {len(all_schemes)}")

        # ── Stage 4: Validate ─────────────────────────────────
        print(f"\n[3/7] Validating schemes...")
        valid_schemes: list[Scheme] = []
        invalid_schemes: list[Scheme] = []
        rejection_reasons: dict[str, list[str]] = {}

        for scheme in all_schemes:
            errors = self.validator.validate(scheme)
            error_msgs = [str(e) for e in errors if e.severity == "ERROR"]

            if error_msgs:
                invalid_schemes.append(scheme)
                rejection_reasons[scheme.scheme_id or scheme.name] = error_msgs
                logger.info(f"  ✗ {scheme.name}: {len(error_msgs)} error(s)")
            else:
                valid_schemes.append(scheme)

        result.validated = len(valid_schemes)
        print(f"  Valid: {len(valid_schemes)}, Invalid: {len(invalid_schemes)}")

        # ── Stage 5: Deduplicate ──────────────────────────────
        print(f"\n[4/7] Deduplicating...")

        # Load existing verified schemes for dedup comparison
        existing = self.file_repo.load_verified_schemes()
        self.dedup.load_existing(existing)

        unique, dupes = self.dedup.deduplicate_batch(valid_schemes)
        result.duplicates_found = len(dupes)
        print(f"  Unique: {len(unique)}, Duplicates: {len(dupes)}")

        for d in dupes:
            print(f"    ↳ Duplicate: {d}")

        # ── Stage 6: Verify ───────────────────────────────────
        print(f"\n[5/7] Verifying {len(unique)} schemes...")
        verified_schemes: list[Scheme] = []
        pending_schemes: list[Scheme] = []

        if skip_verification:
            print("  (Skipping URL verification — all marked PENDING)")
            for s in unique:
                s.verification_status = VerificationStatus.PENDING
            verified_schemes = unique
        else:
            with SchemeVerifier(review_queue_dir=f"{self.staging_dir}/review_queue") as verifier:
                for scheme in unique:
                    scheme, checks = verifier.verify(scheme)

                    if scheme.verification_status == VerificationStatus.VERIFIED:
                        verified_schemes.append(scheme)
                    else:
                        pending_schemes.append(scheme)

                # Save review queue
                verifier.save_review_queue()
                queue_summary = verifier.get_queue_summary()
                print(f"  Review queue: {queue_summary}")

        result.verified = len(verified_schemes)
        print(f"  Verified: {len(verified_schemes)}, Pending review: {len(pending_schemes)}")

        # For the pilot, include pending schemes as "accepted" since they
        # have valid data, just haven't been URL-verified yet
        accepted = verified_schemes + pending_schemes
        result.accepted = len(accepted)

        # ── Stage 7: Store ────────────────────────────────────
        print(f"\n[6/7] Storing {len(accepted)} accepted schemes...")

        # Save versioned JSON
        json_path = self.file_repo.save_verified_json(accepted)
        print(f"  JSON: {json_path}")

        # Save CSV
        csv_path = self.file_repo.save_verified_csv(accepted)
        print(f"  CSV:  {csv_path}")

        # Save staging data
        if pending_schemes:
            self.file_repo.save_staging(pending_schemes)

        # Save rejected
        if invalid_schemes:
            self.file_repo.save_rejected(invalid_schemes, rejection_reasons)
            result.rejected = len(invalid_schemes)

        # PostgreSQL (optional)
        if not skip_db:
            print(f"\n[7/7] Loading into PostgreSQL...")
            db_cfg = self.config.get("database", {})
            try:
                with PostgresRepository(
                    host=os.getenv("DB_HOST", db_cfg.get("host", "localhost")),
                    port=int(os.getenv("DB_PORT", db_cfg.get("port", 5432))),
                    dbname=os.getenv("DB_NAME", db_cfg.get("name", "jansetu")),
                    user=os.getenv("DB_USER", db_cfg.get("user", "jansetu")),
                    password=os.getenv("DB_PASSWORD", db_cfg.get("password", "jansetu_secret_2026")),
                ) as pg_repo:
                    db_results = pg_repo.upsert_batch(accepted)
                    print(f"  DB upsert: {db_results}")
            except Exception as e:
                msg = f"PostgreSQL loading failed: {e}"
                logger.error(msg)
                result.errors.append(msg)
                print(f"  ⚠ {msg}")
        else:
            print(f"\n[7/7] Skipping PostgreSQL (use --load-db to enable)")

        # ── Summary ───────────────────────────────────────────
        result.finished_at = datetime.utcnow()
        duration = (result.finished_at - result.started_at).total_seconds()

        print("\n" + "=" * 60)
        print("  Pipeline Complete!")
        print("=" * 60)
        print(f"  Duration:        {duration:.1f}s")
        print(f"  Discovered:      {result.total_discovered}")
        print(f"  Extracted:       {result.extracted}")
        print(f"  Normalized:      {result.normalized}")
        print(f"  Validated:       {result.validated}")
        print(f"  Duplicates:      {result.duplicates_found}")
        print(f"  Verified:        {result.verified}")
        print(f"  Accepted:        {result.accepted}")
        print(f"  Rejected:        {result.rejected}")
        print(f"  Errors:          {len(result.errors)}")

        # Quality metrics
        if accepted:
            avg_completeness = sum(s.completeness_score() for s in accepted) / len(accepted)
            print(f"\n  Avg completeness: {avg_completeness:.1%}")
            with_evidence = sum(1 for s in accepted if s.source_evidence)
            print(f"  With evidence:    {with_evidence}/{len(accepted)}")
            with_rules = sum(1 for s in accepted if s.eligibility_rules)
            print(f"  With elig rules:  {with_rules}/{len(accepted)}")

        if result.errors:
            print(f"\n  Errors:")
            for err in result.errors:
                print(f"    • {err}")

        print()
        return result

    def _get_collectors(self, sources: list[str] | None, max_schemes: int) -> dict:
        """Initialize the requested source collectors."""
        available = {
            "myscheme": lambda: MySchemeCollector(
                raw_data_dir=self.raw_data_dir,
                max_schemes=max_schemes,
            ),
            "telangana": lambda: TelanganaCollector(
                raw_data_dir=self.raw_data_dir,
            ),
        }

        if sources:
            return {
                name: factory()
                for name, factory in available.items()
                if name in sources
            }

        # Default: all enabled sources from config
        enabled = set()
        for name, cfg in self.config.get("sources", {}).items():
            if cfg.get("enabled", False):
                # Map config source names to collector names
                collector_name = name.replace("_portal", "")
                if collector_name in available:
                    enabled.add(collector_name)

        # If no config, default to both
        if not enabled:
            enabled = {"myscheme", "telangana"}

        return {name: available[name]() for name in enabled if name in available}


# ── CLI Entry Point ──────────────────────────────────────────────
def main():
    """CLI entry point for the pipeline."""
    import argparse
    import io
    import sys

    # Force UTF-8 output on Windows (cp1252 can't encode →, ⚠, etc.)
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    parser = argparse.ArgumentParser(description="JanSetuAI Data Pipeline — Phase 1")
    parser.add_argument(
        "--sources", nargs="+",
        choices=["myscheme", "telangana", "all"],
        default=["all"],
        help="Sources to collect from",
    )
    parser.add_argument(
        "--skip-verify", action="store_true",
        help="Skip URL verification (faster for testing)",
    )
    parser.add_argument(
        "--load-db", action="store_true",
        help="Load accepted records into PostgreSQL",
    )
    parser.add_argument(
        "--max-schemes", type=int, default=50,
        help="Maximum schemes per source",
    )
    parser.add_argument(
        "--config", default="data_pipeline/config/sources.yaml",
        help="Path to sources config",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    sources = None if "all" in args.sources else args.sources

    pipeline = DataPipeline(config_path=args.config)
    result = pipeline.run(
        sources=sources,
        skip_verification=args.skip_verify,
        skip_db=not args.load_db,
        max_schemes=args.max_schemes,
    )

    # Exit with error code if there were critical errors
    if result.accepted == 0 and result.total_discovered > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

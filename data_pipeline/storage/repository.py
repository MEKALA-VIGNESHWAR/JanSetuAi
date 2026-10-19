"""
JanSetuAI — Storage Repository
================================
Stores scheme records in JSON/CSV (file-based) and PostgreSQL.
Handles versioned exports and database upserts.
"""

from __future__ import annotations

import csv
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from data_pipeline.validation.schema import Scheme, EligibilityRule

logger = logging.getLogger(__name__)


class FileRepository:
    """
    File-based storage for scheme records.
    Supports versioned JSON and CSV exports.
    """

    def __init__(
        self,
        verified_dir: str = "data/verified",
        rejected_dir: str = "data/rejected",
        staging_dir: str = "data/staging",
    ):
        self.verified_dir = Path(verified_dir)
        self.rejected_dir = Path(rejected_dir)
        self.staging_dir = Path(staging_dir)

        for d in (self.verified_dir, self.rejected_dir, self.staging_dir):
            d.mkdir(parents=True, exist_ok=True)

    def save_verified_json(self, schemes: list[Scheme], version: str = "") -> str:
        """Save verified schemes as versioned JSON."""
        if not version:
            version = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        output_path = self.verified_dir / f"schemes_v{version}.json"
        data = [self._scheme_to_dict(s) for s in schemes]

        output_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        logger.info(f"Saved {len(schemes)} verified schemes to {output_path}")
        return str(output_path)

    def save_verified_csv(self, schemes: list[Scheme], version: str = "") -> str:
        """Save verified schemes as CSV."""
        if not version:
            version = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        output_path = self.verified_dir / f"schemes_v{version}.csv"

        csv_fields = [
            "scheme_id", "slug", "name", "short_description", "opportunity_type",
            "category", "government_level", "state", "scheme_status",
            "benefit_type", "benefit_amount", "eligibility_summary",
            "application_url", "application_mode", "department",
            "source_url", "verification_status", "last_verified",
            "completeness_score",
        ]

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
            writer.writeheader()

            for scheme in schemes:
                row = self._scheme_to_dict(scheme)
                row["completeness_score"] = scheme.completeness_score()
                # Flatten enums to string values
                for k, v in row.items():
                    if hasattr(v, "value"):
                        row[k] = v.value
                writer.writerow(row)

        logger.info(f"Saved {len(schemes)} schemes to CSV: {output_path}")
        return str(output_path)

    def save_rejected(self, schemes: list[Scheme], reasons: dict[str, list[str]]) -> str:
        """Save rejected schemes with rejection reasons."""
        output_path = self.rejected_dir / f"rejected_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

        data = []
        for scheme in schemes:
            entry = self._scheme_to_dict(scheme)
            entry["rejection_reasons"] = reasons.get(scheme.scheme_id or scheme.name, [])
            data.append(entry)

        output_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        logger.info(f"Saved {len(schemes)} rejected schemes to {output_path}")
        return str(output_path)

    def save_staging(self, schemes: list[Scheme]) -> str:
        """Save schemes to staging area (pre-verification)."""
        output_path = self.staging_dir / f"staging_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

        data = [self._scheme_to_dict(s) for s in schemes]
        output_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        logger.info(f"Saved {len(schemes)} schemes to staging: {output_path}")
        return str(output_path)

    def load_verified_schemes(self) -> list[Scheme]:
        """Load the latest verified schemes from disk."""
        json_files = sorted(self.verified_dir.glob("schemes_v*.json"), reverse=True)
        if not json_files:
            return []

        latest = json_files[0]
        data = json.loads(latest.read_text(encoding="utf-8"))
        schemes = []
        for item in data:
            try:
                schemes.append(Scheme(**item))
            except Exception as e:
                logger.warning(f"Failed to load scheme from {latest}: {e}")

        logger.info(f"Loaded {len(schemes)} schemes from {latest}")
        return schemes

    def _scheme_to_dict(self, scheme: Scheme) -> dict:
        """Convert Scheme to a JSON-serializable dict."""
        d = scheme.model_dump(mode="json")
        return d


class PostgresRepository:
    """
    PostgreSQL storage for scheme records.
    Uses the existing `opportunities` and `eligibility_rules` tables.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "jansetu",
        user: str = "jansetu",
        password: str = "jansetu_secret_2026",
    ):
        self.connection_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password,
        }
        self._conn = None

    def connect(self):
        """Establish database connection."""
        try:
            import psycopg2
            self._conn = psycopg2.connect(**self.connection_params)
            logger.info("Connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    def upsert_scheme(self, scheme: Scheme) -> int | None:
        """
        Insert or update a scheme in the opportunities table.
        Uses slug as the unique key for upsert.
        Returns the opportunity id.
        """
        if not self._conn:
            self.connect()

        cur = self._conn.cursor()

        # Map Scheme to opportunities table columns
        opp_data = {
            "name": scheme.name,
            "slug": scheme.slug,
            "description": scheme.description or "",
            "short_description": scheme.short_description or "",
            "type": scheme.opportunity_type.value if scheme.opportunity_type else "SCHEME",
            "category": scheme.category.value if scheme.category else "GENERAL",
            "sub_category": scheme.sub_category,
            "government_level": scheme.government_level.value if scheme.government_level else None,
            "state": scheme.state,
            "districts": ",".join(scheme.districts) if scheme.districts else None,
            "target_groups": json.dumps(scheme.target_groups) if scheme.target_groups else None,
            "min_age": scheme.age_range.min_age if scheme.age_range else None,
            "max_age": scheme.age_range.max_age if scheme.age_range else None,
            "gender_restriction": scheme.gender_restriction or "ALL",
            "benefits": scheme.benefits or "",
            "benefit_type": scheme.benefit_type.value if scheme.benefit_type else None,
            "benefit_amount": scheme.benefit_amount or "",
            "eligibility_summary": scheme.eligibility_summary or "",
            "required_documents": json.dumps(scheme.required_documents) if scheme.required_documents else None,
            "application_url": scheme.application_url or "",
            "application_steps": json.dumps(scheme.application_steps) if scheme.application_steps else None,
            "application_deadline": scheme.application_deadline,
            "official_source": scheme.official_source or scheme.department or "",
            "source_url": scheme.source_url or "",
            "last_verified": scheme.last_verified,
            "verification_status": scheme.verification_status.value if scheme.verification_status else "PENDING",
            "status": scheme.scheme_status.value if scheme.scheme_status else "ACTIVE",
            "tags": ",".join(scheme.tags) if scheme.tags else None,
            "icon": scheme.icon or "",
        }

        try:
            # Upsert using slug as unique key
            cur.execute("""
                INSERT INTO opportunities (
                    name, slug, description, short_description, type, category,
                    sub_category, government_level, state, districts, target_groups,
                    min_age, max_age, gender_restriction, benefits, benefit_type,
                    benefit_amount, eligibility_summary, required_documents,
                    application_url, application_steps, application_deadline,
                    official_source, source_url, last_verified, verification_status,
                    status, tags, icon, created_at, updated_at
                ) VALUES (
                    %(name)s, %(slug)s, %(description)s, %(short_description)s,
                    %(type)s, %(category)s, %(sub_category)s, %(government_level)s,
                    %(state)s, %(districts)s, %(target_groups)s, %(min_age)s,
                    %(max_age)s, %(gender_restriction)s, %(benefits)s, %(benefit_type)s,
                    %(benefit_amount)s, %(eligibility_summary)s, %(required_documents)s,
                    %(application_url)s, %(application_steps)s, %(application_deadline)s,
                    %(official_source)s, %(source_url)s, %(last_verified)s,
                    %(verification_status)s, %(status)s, %(tags)s, %(icon)s,
                    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
                )
                ON CONFLICT (slug) DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    short_description = EXCLUDED.short_description,
                    benefits = EXCLUDED.benefits,
                    benefit_type = EXCLUDED.benefit_type,
                    benefit_amount = EXCLUDED.benefit_amount,
                    eligibility_summary = EXCLUDED.eligibility_summary,
                    required_documents = EXCLUDED.required_documents,
                    application_url = EXCLUDED.application_url,
                    application_steps = EXCLUDED.application_steps,
                    source_url = EXCLUDED.source_url,
                    last_verified = EXCLUDED.last_verified,
                    verification_status = EXCLUDED.verification_status,
                    status = EXCLUDED.status,
                    tags = EXCLUDED.tags,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id
            """, opp_data)

            row = cur.fetchone()
            opp_id = row[0] if row else None

            # Upsert eligibility rules
            if opp_id and scheme.eligibility_rules:
                self._upsert_eligibility_rules(cur, opp_id, scheme.eligibility_rules)

            self._conn.commit()
            logger.info(f"Upserted scheme '{scheme.name}' with id={opp_id}")
            return opp_id

        except Exception as e:
            self._conn.rollback()
            logger.error(f"Failed to upsert scheme '{scheme.name}': {e}")
            return None

    def _upsert_eligibility_rules(self, cur, opp_id: int, rules: list[EligibilityRule]):
        """Insert eligibility rules for an opportunity."""
        # Delete existing rules for this opportunity
        cur.execute("DELETE FROM eligibility_rules WHERE opportunity_id = %s", (opp_id,))

        for i, rule in enumerate(rules):
            cur.execute("""
                INSERT INTO eligibility_rules (
                    opportunity_id, rule_field, rule_operator, rule_value,
                    rule_group, is_mandatory, description
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                opp_id,
                rule.field,
                rule.operator,
                rule.value,
                0,  # default group
                rule.is_mandatory,
                rule.description or "",
            ))

    def upsert_batch(self, schemes: list[Scheme]) -> dict[str, int]:
        """Upsert a batch of schemes. Returns success/failure counts."""
        results = {"success": 0, "failed": 0}
        for scheme in schemes:
            opp_id = self.upsert_scheme(scheme)
            if opp_id:
                results["success"] += 1
            else:
                results["failed"] += 1
        return results

    def get_existing_slugs(self) -> set[str]:
        """Get all existing slugs from the database."""
        if not self._conn:
            self.connect()

        cur = self._conn.cursor()
        cur.execute("SELECT slug FROM opportunities WHERE slug IS NOT NULL")
        return {row[0] for row in cur.fetchall()}

    def get_scheme_count(self) -> int:
        """Get total number of schemes in the database."""
        if not self._conn:
            self.connect()

        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM opportunities")
        return cur.fetchone()[0]

    def close(self):
        """Close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None
            logger.info("PostgreSQL connection closed")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

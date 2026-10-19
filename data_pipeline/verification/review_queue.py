"""
JanSetuAI — Verification / Review Queue
=========================================
Verifies scheme information against official sources.
Manages a review queue for records needing human attention.
"""

from __future__ import annotations

import json
import logging
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

import httpx

from data_pipeline.validation.schema import Scheme, VerificationStatus

logger = logging.getLogger(__name__)


class VerificationCheck:
    """Result of a single verification check."""

    def __init__(
        self,
        check_name: str,
        passed: bool,
        details: str = "",
        evidence_url: str = "",
    ):
        self.check_name = check_name
        self.passed = passed
        self.details = details
        self.evidence_url = evidence_url
        self.checked_at = datetime.utcnow()

    def __repr__(self):
        status = "✓" if self.passed else "✗"
        return f"{status} {self.check_name}: {self.details}"


class ReviewItem:
    """An item in the review queue."""

    def __init__(
        self,
        scheme: Scheme,
        reason: str,
        checks: list[VerificationCheck],
        priority: str = "normal",
    ):
        self.scheme = scheme
        self.reason = reason
        self.checks = checks
        self.priority = priority  # high, normal, low
        self.created_at = datetime.utcnow()
        self.status = "pending"   # pending, reviewed, resolved

    def to_dict(self) -> dict:
        return {
            "scheme_name": self.scheme.name,
            "scheme_slug": self.scheme.slug,
            "reason": self.reason,
            "priority": self.priority,
            "status": self.status,
            "checks": [
                {
                    "name": c.check_name,
                    "passed": c.passed,
                    "details": c.details,
                }
                for c in self.checks
            ],
            "created_at": self.created_at.isoformat(),
        }


class SchemeVerifier:
    """
    Verifies scheme records against official sources.
    Runs automated checks and queues uncertain records for review.
    """

    def __init__(self, review_queue_dir: str = "data/staging/review_queue"):
        self.review_queue_dir = Path(review_queue_dir)
        self.review_queue_dir.mkdir(parents=True, exist_ok=True)
        self.review_queue: list[ReviewItem] = []
        self._http = httpx.Client(
            timeout=httpx.Timeout(15.0),
            follow_redirects=True,
            headers={"User-Agent": "JanSetuAI-Verifier/1.0"},
        )

    def verify(self, scheme: Scheme) -> tuple[Scheme, list[VerificationCheck]]:
        """
        Run all verification checks on a scheme.
        Updates scheme.verification_status based on results.
        Returns (updated_scheme, checks).
        """
        checks: list[VerificationCheck] = []

        # 1. Check source URL is accessible
        checks.append(self._check_url_accessible(scheme.source_url, "source_url"))

        # 2. Check application URL is accessible
        if scheme.application_url:
            checks.append(self._check_url_accessible(scheme.application_url, "application_url"))

        # 3. Check required fields have evidence
        checks.append(self._check_source_evidence(scheme))

        # 4. Check scheme status coherence
        checks.append(self._check_status_coherence(scheme))

        # 5. Check completeness threshold
        checks.append(self._check_completeness(scheme))

        # Determine overall status
        errors = [c for c in checks if not c.passed]
        critical_failures = [c for c in errors if c.check_name in ("source_url_accessible", "has_source_evidence")]

        if not errors:
            scheme.verification_status = VerificationStatus.VERIFIED
            scheme.last_verified = date.today()
            scheme.verified_by = "automated_pipeline"
        elif critical_failures:
            scheme.verification_status = VerificationStatus.NEEDS_REVIEW
            self._add_to_review_queue(scheme, "Critical verification checks failed", checks)
        else:
            scheme.verification_status = VerificationStatus.PENDING
            self._add_to_review_queue(scheme, "Some verification checks failed", checks)

        return scheme, checks

    def _check_url_accessible(self, url: str | None, field_name: str) -> VerificationCheck:
        """Check if a URL returns a successful response."""
        if not url:
            return VerificationCheck(
                check_name=f"{field_name}_accessible",
                passed=False,
                details=f"No {field_name} provided",
            )

        try:
            resp = self._http.head(url, follow_redirects=True)
            if resp.status_code < 400:
                return VerificationCheck(
                    check_name=f"{field_name}_accessible",
                    passed=True,
                    details=f"URL returned {resp.status_code}",
                    evidence_url=url,
                )
            else:
                return VerificationCheck(
                    check_name=f"{field_name}_accessible",
                    passed=False,
                    details=f"URL returned {resp.status_code}",
                    evidence_url=url,
                )
        except Exception as e:
            return VerificationCheck(
                check_name=f"{field_name}_accessible",
                passed=False,
                details=f"Error accessing URL: {str(e)[:100]}",
                evidence_url=url,
            )

    def _check_source_evidence(self, scheme: Scheme) -> VerificationCheck:
        """Check that the scheme has source evidence."""
        if scheme.source_evidence and len(scheme.source_evidence) > 0:
            return VerificationCheck(
                check_name="has_source_evidence",
                passed=True,
                details=f"{len(scheme.source_evidence)} evidence record(s)",
            )
        return VerificationCheck(
            check_name="has_source_evidence",
            passed=False,
            details="No source evidence records",
        )

    def _check_status_coherence(self, scheme: Scheme) -> VerificationCheck:
        """Check that scheme status is explicitly set."""
        from data_pipeline.validation.schema import SchemeStatus
        if scheme.scheme_status == SchemeStatus.UNKNOWN:
            return VerificationCheck(
                check_name="status_known",
                passed=False,
                details="Scheme status is UNKNOWN — needs review",
            )
        return VerificationCheck(
            check_name="status_known",
            passed=True,
            details=f"Status: {scheme.scheme_status.value}",
        )

    def _check_completeness(self, scheme: Scheme) -> VerificationCheck:
        """Check completeness score meets minimum threshold."""
        score = scheme.completeness_score()
        threshold = 0.5

        return VerificationCheck(
            check_name="completeness",
            passed=score >= threshold,
            details=f"Completeness: {score:.1%} (minimum: {threshold:.0%})",
        )

    def _add_to_review_queue(
        self,
        scheme: Scheme,
        reason: str,
        checks: list[VerificationCheck],
    ):
        """Add a scheme to the review queue."""
        item = ReviewItem(
            scheme=scheme,
            reason=reason,
            checks=checks,
            priority="high" if any(not c.passed and c.check_name == "source_url_accessible" for c in checks) else "normal",
        )
        self.review_queue.append(item)

    def save_review_queue(self):
        """Persist the review queue to disk."""
        if not self.review_queue:
            return

        queue_data = [item.to_dict() for item in self.review_queue]
        output_path = self.review_queue_dir / f"review_queue_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

        output_path.write_text(
            json.dumps(queue_data, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        logger.info(f"Saved review queue with {len(self.review_queue)} items to {output_path}")

    def get_queue_summary(self) -> dict:
        """Return summary of the review queue."""
        return {
            "total": len(self.review_queue),
            "high_priority": sum(1 for i in self.review_queue if i.priority == "high"),
            "normal_priority": sum(1 for i in self.review_queue if i.priority == "normal"),
            "pending": sum(1 for i in self.review_queue if i.status == "pending"),
        }

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

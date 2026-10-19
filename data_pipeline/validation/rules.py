"""
JanSetuAI — Validation Rules
==============================
Validates scheme records for required fields, field types,
data consistency, and URL validity.
"""

from __future__ import annotations

import logging
import re
from typing import Any
from urllib.parse import urlparse

from data_pipeline.validation.schema import Scheme, VerificationStatus

logger = logging.getLogger(__name__)


class ValidationError:
    """A single validation issue."""
    def __init__(self, field: str, severity: str, message: str):
        self.field = field
        self.severity = severity   # ERROR, WARNING, INFO
        self.message = message

    def __repr__(self):
        return f"[{self.severity}] {self.field}: {self.message}"


class SchemeValidator:
    """
    Validates Scheme records against quality rules.
    Returns a list of ValidationErrors.
    """

    # Fields required for a scheme to be published
    REQUIRED_FIELDS = [
        "name",
        "description",
        "eligibility_summary",
        "source_url",
        "benefits",
    ]

    # Fields strongly recommended
    RECOMMENDED_FIELDS = [
        "category",
        "government_level",
        "department",
        "benefit_type",
        "scheme_status",
    ]

    def validate(self, scheme: Scheme) -> list[ValidationError]:
        """Run all validation checks and return issues."""
        errors: list[ValidationError] = []

        errors.extend(self._check_required_fields(scheme))
        errors.extend(self._check_field_lengths(scheme))
        errors.extend(self._check_urls(scheme))
        errors.extend(self._check_data_consistency(scheme))
        errors.extend(self._check_recommended_fields(scheme))

        return errors

    def is_publishable(self, scheme: Scheme) -> bool:
        """Check if a scheme has zero ERROR-severity issues."""
        errors = self.validate(scheme)
        return not any(e.severity == "ERROR" for e in errors)

    def _check_required_fields(self, scheme: Scheme) -> list[ValidationError]:
        """Ensure all required fields are present."""
        errors = []
        for field in self.REQUIRED_FIELDS:
            val = getattr(scheme, field, None)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors.append(ValidationError(
                    field=field,
                    severity="ERROR",
                    message=f"Required field '{field}' is empty or missing",
                ))
        return errors

    def _check_recommended_fields(self, scheme: Scheme) -> list[ValidationError]:
        """Flag missing recommended fields as warnings."""
        errors = []
        for field in self.RECOMMENDED_FIELDS:
            val = getattr(scheme, field, None)
            if val is None or (isinstance(val, str) and not val.strip()):
                errors.append(ValidationError(
                    field=field,
                    severity="WARNING",
                    message=f"Recommended field '{field}' is missing",
                ))
        return errors

    def _check_field_lengths(self, scheme: Scheme) -> list[ValidationError]:
        """Validate field length constraints."""
        errors = []

        if scheme.name and len(scheme.name) < 5:
            errors.append(ValidationError(
                field="name",
                severity="WARNING",
                message=f"Scheme name seems too short: '{scheme.name}'",
            ))

        if scheme.name and len(scheme.name) > 500:
            errors.append(ValidationError(
                field="name",
                severity="ERROR",
                message="Scheme name exceeds 500 characters",
            ))

        if scheme.description and len(scheme.description) < 20:
            errors.append(ValidationError(
                field="description",
                severity="WARNING",
                message="Description seems too short to be useful",
            ))

        if scheme.eligibility_summary and len(scheme.eligibility_summary) < 10:
            errors.append(ValidationError(
                field="eligibility_summary",
                severity="WARNING",
                message="Eligibility summary seems too short",
            ))

        return errors

    def _check_urls(self, scheme: Scheme) -> list[ValidationError]:
        """Validate URL formats (not reachability — that's verification)."""
        errors = []

        for field_name in ("source_url", "application_url", "source_document_url"):
            url = getattr(scheme, field_name, None)
            if url and isinstance(url, str) and url.strip():
                if not self._is_valid_url(url):
                    errors.append(ValidationError(
                        field=field_name,
                        severity="ERROR",
                        message=f"Invalid URL format: {url}",
                    ))

        return errors

    def _check_data_consistency(self, scheme: Scheme) -> list[ValidationError]:
        """Check for logical consistency in scheme data."""
        errors = []

        # Age range consistency
        if scheme.age_range:
            if scheme.age_range.min_age and scheme.age_range.max_age:
                if scheme.age_range.min_age > scheme.age_range.max_age:
                    errors.append(ValidationError(
                        field="age_range",
                        severity="ERROR",
                        message=f"min_age ({scheme.age_range.min_age}) > max_age ({scheme.age_range.max_age})",
                    ))
            if scheme.age_range.min_age and scheme.age_range.min_age < 0:
                errors.append(ValidationError(
                    field="age_range",
                    severity="ERROR",
                    message="min_age cannot be negative",
                ))
            if scheme.age_range.max_age and scheme.age_range.max_age > 120:
                errors.append(ValidationError(
                    field="age_range",
                    severity="WARNING",
                    message=f"max_age ({scheme.age_range.max_age}) seems unrealistically high",
                ))

        # Income limit consistency
        if scheme.income_limit and scheme.income_limit.amount:
            if scheme.income_limit.amount < 0:
                errors.append(ValidationError(
                    field="income_limit",
                    severity="ERROR",
                    message="Income limit cannot be negative",
                ))
            if scheme.income_limit.amount > 100_000_000:  # 10 crore
                errors.append(ValidationError(
                    field="income_limit",
                    severity="WARNING",
                    message=f"Income limit ₹{scheme.income_limit.amount:,} seems unusually high",
                ))

        # Source evidence for published schemes
        if scheme.verification_status == VerificationStatus.VERIFIED:
            if not scheme.source_evidence:
                errors.append(ValidationError(
                    field="source_evidence",
                    severity="ERROR",
                    message="Verified scheme must have source evidence",
                ))

        return errors

    def _is_valid_url(self, url: str) -> bool:
        """Check if URL has valid format."""
        try:
            parsed = urlparse(url)
            return parsed.scheme in ("http", "https") and bool(parsed.netloc)
        except Exception:
            return False

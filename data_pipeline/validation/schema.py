"""
JanSetuAI Data Pipeline — Pydantic Schema
==========================================
Defines the canonical Scheme data model with all fields required
for trustworthy recommendations. Separates raw source text from
normalized eligibility rules for audit trail.
"""

from __future__ import annotations

import hashlib
import re
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


def utc_now() -> datetime:
    """Return timezone-aware current UTC time."""
    return datetime.now(timezone.utc)


# ── Enums ───────────────────────────────────────────────────────
class SchemeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    UPCOMING = "UPCOMING"
    SUSPENDED = "SUSPENDED"
    UNKNOWN = "UNKNOWN"


class VerificationStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    REJECTED = "REJECTED"


class BenefitType(str, Enum):
    FINANCIAL = "FINANCIAL"
    SCHOLARSHIP = "SCHOLARSHIP"
    SUBSIDY = "SUBSIDY"
    LOAN = "LOAN"
    INSURANCE = "INSURANCE"
    TRAINING = "TRAINING"
    JOB = "JOB"
    HOUSING = "HOUSING"
    EQUIPMENT = "EQUIPMENT"
    SERVICE = "SERVICE"
    OTHER = "OTHER"


class GovernmentLevel(str, Enum):
    CENTRAL = "CENTRAL"
    STATE = "STATE"
    DISTRICT = "DISTRICT"


class ApplicationMode(str, Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    BOTH = "BOTH"
    UNKNOWN = "UNKNOWN"


class OpportunityType(str, Enum):
    SCHEME = "SCHEME"
    SCHOLARSHIP = "SCHOLARSHIP"
    JOB = "JOB"
    SUBSIDY = "SUBSIDY"
    TRAINING = "TRAINING"
    LOAN = "LOAN"
    PROGRAM = "PROGRAM"


class Category(str, Enum):
    FARMER = "FARMER"
    STUDENT = "STUDENT"
    JOB_SEEKER = "JOB_SEEKER"
    WOMEN = "WOMEN"
    ENTREPRENEUR = "ENTREPRENEUR"
    GENERAL = "GENERAL"
    SENIOR_CITIZEN = "SENIOR_CITIZEN"
    MINORITY = "MINORITY"


# ── Sub-models ──────────────────────────────────────────────────
class IncomeLimit(BaseModel):
    """Structured income limit instead of raw text."""
    amount: Optional[int] = None           # e.g. 250000
    currency: str = "INR"
    period: str = "annual"                 # annual, monthly
    basis: str = "family"                  # family, individual
    raw_text: Optional[str] = None         # original source text


class AgeRange(BaseModel):
    """Age eligibility with exceptions support."""
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    exceptions: Optional[str] = None       # e.g. "up to 45 for women"


class EligibilityRule(BaseModel):
    """A single structured eligibility condition."""
    field: str                             # e.g. 'occupation', 'social_category'
    operator: str                          # EQ, NEQ, IN, GTE, LTE, etc.
    value: str                             # e.g. 'FARMER', 'SC,ST'
    is_mandatory: bool = True
    description: Optional[str] = None      # human readable
    source_evidence: Optional[str] = None  # exact text from official source


class SourceEvidence(BaseModel):
    """Track where a piece of information came from."""
    url: str
    retrieved_at: datetime
    snapshot_path: Optional[str] = None    # path to raw snapshot
    relevant_text: Optional[str] = None    # extracted passage


# ── Main Scheme Model ──────────────────────────────────────────
class Scheme(BaseModel):
    """
    The canonical scheme record. Every field that JanSetuAI needs
    to make recommendations lives here. Unknown values are null —
    never assumed.
    """
    # Identity
    scheme_id: Optional[str] = None        # auto-generated unique id
    official_scheme_code: Optional[str] = None
    slug: Optional[str] = None

    # Basic info
    name: str
    short_description: Optional[str] = None
    description: Optional[str] = None

    # Classification
    opportunity_type: OpportunityType = OpportunityType.SCHEME
    category: Optional[Category] = None
    sub_category: Optional[str] = None
    tags: list[str] = Field(default_factory=list)

    # Government
    government_level: Optional[GovernmentLevel] = None
    state: Optional[str] = None              # null = all india
    districts: list[str] = Field(default_factory=list)

    # Status
    scheme_status: SchemeStatus = SchemeStatus.UNKNOWN

    # Target demographics
    target_groups: list[str] = Field(default_factory=list)
    age_range: Optional[AgeRange] = None
    gender_restriction: Optional[str] = None   # ALL, MALE, FEMALE

    # Benefits
    benefits: Optional[str] = None
    benefit_type: Optional[BenefitType] = None
    benefit_amount: Optional[str] = None

    # Eligibility — raw from source vs structured rules
    eligibility_summary: Optional[str] = None   # what the official source says
    eligibility_rules: list[EligibilityRule] = Field(default_factory=list)
    exclusions: list[str] = Field(default_factory=list)
    income_limit: Optional[IncomeLimit] = None

    # Documents
    required_documents: list[str] = Field(default_factory=list)

    # Application
    application_url: Optional[str] = None
    application_steps: list[str] = Field(default_factory=list)
    application_mode: ApplicationMode = ApplicationMode.UNKNOWN
    application_deadline: Optional[str] = None

    # Responsible entity
    department: Optional[str] = None
    official_source: Optional[str] = None

    # Source & verification
    source_url: Optional[str] = None
    source_document_url: Optional[str] = None  # link to official PDF/guideline
    source_evidence: list[SourceEvidence] = Field(default_factory=list)

    # Verification
    verification_status: VerificationStatus = VerificationStatus.PENDING
    verified_by: Optional[str] = None
    last_verified: Optional[date] = None

    # Metadata
    icon: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    @model_validator(mode="after")
    def generate_scheme_id(self) -> "Scheme":
        """Auto-generate scheme_id from name if not set."""
        if not self.scheme_id and self.name:
            raw = self.name.lower().strip()
            self.scheme_id = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return self

    @model_validator(mode="after")
    def generate_slug(self) -> "Scheme":
        """Auto-generate slug from name if not set."""
        if not self.slug and self.name:
            slug = self.name.lower().strip()
            slug = re.sub(r"[^a-z0-9\s-]", "", slug)
            slug = re.sub(r"[\s]+", "-", slug)
            slug = slug.strip("-")[:100]
            self.slug = slug
        return self

    def completeness_score(self) -> float:
        """
        Calculate how complete this record is (0.0 – 1.0).
        Required fields weigh more than optional ones.
        """
        required = [
            ("name", 10),
            ("description", 8),
            ("eligibility_summary", 9),
            ("benefits", 8),
            ("source_url", 10),
            ("department", 5),
            ("government_level", 5),
            ("category", 5),
            ("scheme_status", 5),
        ]
        optional = [
            ("short_description", 3),
            ("benefit_type", 3),
            ("benefit_amount", 3),
            ("application_url", 4),
            ("application_mode", 2),
            ("required_documents", 4),
            ("eligibility_rules", 5),
            ("age_range", 3),
            ("income_limit", 3),
            ("target_groups", 3),
            ("exclusions", 2),
            ("icon", 1),
        ]
        total_weight = sum(w for _, w in required) + sum(w for _, w in optional)
        earned = 0.0
        for field_name, weight in required + optional:
            val = getattr(self, field_name, None)
            if val is not None and val != [] and val != "":
                earned += weight
        return round(earned / total_weight, 3)


# ── Raw Source Snapshot ─────────────────────────────────────────
class RawSourceSnapshot(BaseModel):
    """Stores the original content retrieved from a source."""
    source_name: str
    url: str
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    content_type: str = "html"    # html, json, pdf
    raw_content: Optional[str] = None
    raw_file_path: Optional[str] = None
    http_status: Optional[int] = None
    headers: dict[str, str] = Field(default_factory=dict)


# ── Pipeline Result ─────────────────────────────────────────────
class PipelineResult(BaseModel):
    """Result of running the pipeline on a batch."""
    total_discovered: int = 0
    extracted: int = 0
    normalized: int = 0
    validated: int = 0
    duplicates_found: int = 0
    verified: int = 0
    accepted: int = 0
    rejected: int = 0
    errors: list[str] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None

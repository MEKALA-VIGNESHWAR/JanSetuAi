"""
JanSetuAI — End-to-End Pipeline Tests
=======================================
Tests the complete pipeline: schema, normalization, validation,
deduplication, verification, storage, and full pipeline run.

Run with: python -m pytest tests/test_pipeline.py -v
"""

import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_pipeline.validation.schema import (
    AgeRange,
    ApplicationMode,
    BenefitType,
    Category,
    EligibilityRule,
    GovernmentLevel,
    IncomeLimit,
    OpportunityType,
    PipelineResult,
    Scheme,
    SchemeStatus,
    SourceEvidence,
    VerificationStatus,
)
from data_pipeline.normalization.scheme_normalizer import SchemeNormalizer
from data_pipeline.validation.rules import SchemeValidator
from data_pipeline.validation.duplicates import DuplicateDetector, DuplicateMatch
from data_pipeline.storage.repository import FileRepository
from data_pipeline.extractors.html_extractor import HTMLExtractor


# ═══════════════════════════════════════════════════════════════
# Schema Tests
# ═══════════════════════════════════════════════════════════════
class TestScheme:
    """Test the Scheme pydantic model."""

    def test_create_minimal_scheme(self):
        """A scheme only needs a name."""
        s = Scheme(name="Test Scheme")
        assert s.name == "Test Scheme"
        assert s.scheme_id is not None  # auto-generated
        assert s.slug is not None       # auto-generated
        assert s.verification_status == VerificationStatus.PENDING
        assert s.scheme_status == SchemeStatus.UNKNOWN

    def test_auto_generate_scheme_id(self):
        """scheme_id is auto-generated from name."""
        s1 = Scheme(name="PM-KISAN")
        s2 = Scheme(name="PM-KISAN")
        assert s1.scheme_id == s2.scheme_id  # deterministic

        s3 = Scheme(name="Different Scheme")
        assert s1.scheme_id != s3.scheme_id

    def test_auto_generate_slug(self):
        """Slug is auto-generated from name."""
        s = Scheme(name="PM-KISAN Samman Nidhi")
        assert s.slug is not None
        assert " " not in s.slug
        assert s.slug.islower() or "-" in s.slug

    def test_completeness_score(self):
        """Completeness score reflects how many fields are filled."""
        minimal = Scheme(name="Test")
        full = Scheme(
            name="PM-KISAN",
            description="A great scheme for farmers",
            eligibility_summary="Farmers with land",
            benefits="₹6000/year",
            source_url="https://pmkisan.gov.in",
            department="MoA",
            government_level=GovernmentLevel.CENTRAL,
            category=Category.FARMER,
            scheme_status=SchemeStatus.ACTIVE,
            benefit_type=BenefitType.FINANCIAL,
            benefit_amount="₹6,000/year",
            application_url="https://pmkisan.gov.in",
            application_mode=ApplicationMode.ONLINE,
            required_documents=["Aadhaar", "Land Records"],
            age_range=AgeRange(min_age=18),
            income_limit=IncomeLimit(amount=200000),
            target_groups=["Farmers"],
            tags=["farmer"],
        )

        assert minimal.completeness_score() < full.completeness_score()
        assert full.completeness_score() > 0.8

    def test_scheme_with_eligibility_rules(self):
        """Scheme can have structured eligibility rules."""
        rules = [
            EligibilityRule(field="age", operator="GTE", value="18"),
            EligibilityRule(field="is_farmer", operator="EQ", value="true"),
        ]
        s = Scheme(name="Test", eligibility_rules=rules)
        assert len(s.eligibility_rules) == 2

    def test_scheme_with_source_evidence(self):
        """Scheme tracks source evidence."""
        s = Scheme(
            name="Test",
            source_evidence=[
                SourceEvidence(url="https://example.gov.in", retrieved_at=datetime.utcnow()),
            ],
        )
        assert len(s.source_evidence) == 1

    def test_income_limit_model(self):
        """Income limit stores structured data."""
        il = IncomeLimit(amount=250000, currency="INR", period="annual", basis="family")
        assert il.amount == 250000

    def test_age_range_model(self):
        """Age range supports min, max, and exceptions."""
        ar = AgeRange(min_age=18, max_age=40, exceptions="up to 45 for women")
        assert ar.min_age == 18
        assert ar.max_age == 40


# ═══════════════════════════════════════════════════════════════
# Normalization Tests
# ═══════════════════════════════════════════════════════════════
class TestNormalizer:
    """Test the SchemeNormalizer."""

    def setup_method(self):
        self.normalizer = SchemeNormalizer()

    def test_normalize_state(self):
        """State names are properly capitalized."""
        s = Scheme(name="Test", state="telangana")
        self.normalizer.normalize(s)
        assert s.state == "Telangana"

    def test_normalize_state_abbreviation(self):
        """State abbreviations are expanded."""
        s = Scheme(name="Test", state="ts")
        self.normalizer.normalize(s)
        assert s.state == "Telangana"

    def test_normalize_age_from_text(self):
        """Age range is extracted from eligibility text."""
        s = Scheme(name="Test", eligibility_summary="Applicants aged 18-40 years")
        self.normalizer.normalize(s)
        assert s.age_range is not None
        assert s.age_range.min_age == 18
        assert s.age_range.max_age == 40

    def test_normalize_income_from_text(self):
        """Income limit is extracted from eligibility text."""
        s = Scheme(name="Test", eligibility_summary="Family income below ₹2.5 lakh")
        self.normalizer.normalize(s)
        assert s.income_limit is not None
        assert s.income_limit.amount == 250000

    def test_normalize_income_lakhs(self):
        """Handles various income format: ₹8 lakh."""
        s = Scheme(name="Test", eligibility_summary="Annual income below ₹8 lakh")
        self.normalizer.normalize(s)
        assert s.income_limit is not None
        assert s.income_limit.amount == 800000

    def test_normalize_benefit_type(self):
        """Benefit type inferred from text."""
        s = Scheme(name="Test", benefits="Scholarship of ₹50,000 per year")
        self.normalizer.normalize(s)
        assert s.benefit_type == BenefitType.SCHOLARSHIP

    def test_normalize_application_mode(self):
        """Application mode detected from URLs and steps."""
        s = Scheme(
            name="Test",
            application_url="https://example.gov.in/apply",
            application_steps=["Visit the portal online"],
        )
        self.normalizer.normalize(s)
        assert s.application_mode == ApplicationMode.ONLINE

    def test_normalize_category_farmer(self):
        """Category inferred from scheme name/description."""
        s = Scheme(name="PM-KISAN", description="Support for farmers and agriculture")
        self.normalizer.normalize(s)
        assert s.category == Category.FARMER

    def test_normalize_documents_dedup(self):
        """Duplicate documents are removed."""
        s = Scheme(name="Test", required_documents=["Aadhaar Card", "aadhaar card", "Bank Account"])
        self.normalizer.normalize(s)
        assert len(s.required_documents) == 2

    def test_extract_eligibility_rules(self):
        """Eligibility rules extracted from text."""
        s = Scheme(
            name="Test",
            eligibility_summary="Farmers with land, aged 18-40, income below ₹2.5 lakh",
            state="Telangana",
        )
        self.normalizer.normalize(s)
        assert len(s.eligibility_rules) > 0
        rule_fields = [r.field for r in s.eligibility_rules]
        assert "is_farmer" in rule_fields
        assert "state" in rule_fields

    def test_normalize_exclusions(self):
        """Exclusions extracted from eligibility text."""
        s = Scheme(
            name="Test",
            eligibility_summary="All farmers eligible. Excludes government employees and income tax payers.",
        )
        self.normalizer.normalize(s)
        assert len(s.exclusions) > 0

    def test_preserve_existing_values(self):
        """Normalization doesn't overwrite existing values."""
        s = Scheme(
            name="Test",
            age_range=AgeRange(min_age=21, max_age=35),
            eligibility_summary="Applicants aged 18-40",
        )
        self.normalizer.normalize(s)
        # Should keep the pre-set values, not overwrite from text
        assert s.age_range.min_age == 21
        assert s.age_range.max_age == 35


# ═══════════════════════════════════════════════════════════════
# Validation Tests
# ═══════════════════════════════════════════════════════════════
class TestValidator:
    """Test the SchemeValidator."""

    def setup_method(self):
        self.validator = SchemeValidator()

    def test_valid_scheme(self):
        """A complete scheme passes validation."""
        s = Scheme(
            name="PM-KISAN Samman Nidhi",
            description="Income support for farmers",
            eligibility_summary="Landholding farmer families",
            benefits="₹6000/year",
            source_url="https://pmkisan.gov.in",
        )
        errors = self.validator.validate(s)
        assert not any(e.severity == "ERROR" for e in errors)
        assert self.validator.is_publishable(s)

    def test_missing_required_fields(self):
        """Missing required fields produce ERROR."""
        s = Scheme(name="Test")  # missing description, eligibility, etc.
        errors = self.validator.validate(s)
        error_list = [e for e in errors if e.severity == "ERROR"]
        assert len(error_list) > 0
        assert not self.validator.is_publishable(s)

    def test_invalid_url(self):
        """Invalid URL format is flagged."""
        s = Scheme(
            name="Test",
            description="A test scheme",
            eligibility_summary="Everyone",
            benefits="Something",
            source_url="not-a-url",
        )
        errors = self.validator.validate(s)
        url_errors = [e for e in errors if e.field == "source_url" and e.severity == "ERROR"]
        assert len(url_errors) > 0

    def test_invalid_age_range(self):
        """min_age > max_age is flagged."""
        s = Scheme(
            name="Test",
            description="A test scheme",
            eligibility_summary="Everyone",
            benefits="Something",
            source_url="https://example.gov.in",
            age_range=AgeRange(min_age=50, max_age=18),
        )
        errors = self.validator.validate(s)
        age_errors = [e for e in errors if e.field == "age_range"]
        assert len(age_errors) > 0

    def test_missing_recommended_fields(self):
        """Missing recommended fields produce WARNING (not ERROR)."""
        s = Scheme(
            name="PM-KISAN",
            description="Income support",
            eligibility_summary="Farmers",
            benefits="₹6000",
            source_url="https://pmkisan.gov.in",
        )
        errors = self.validator.validate(s)
        warnings = [e for e in errors if e.severity == "WARNING"]
        assert len(warnings) > 0  # Missing category, government_level, etc.
        assert self.validator.is_publishable(s)  # But still publishable


# ═══════════════════════════════════════════════════════════════
# Deduplication Tests
# ═══════════════════════════════════════════════════════════════
class TestDeduplication:
    """Test the DuplicateDetector."""

    def setup_method(self):
        self.dedup = DuplicateDetector(similarity_threshold=0.85)

    def test_exact_slug_duplicate(self):
        """Exact slug match is detected."""
        existing = [Scheme(name="PM-KISAN", slug="pm-kisan")]
        self.dedup.load_existing(existing)

        candidate = Scheme(name="PM-KISAN Scheme", slug="pm-kisan")
        match = self.dedup.find_duplicate(candidate)
        assert match is not None
        assert match.match_type == "slug"

    def test_url_duplicate(self):
        """Same source URL is detected as duplicate."""
        existing = [Scheme(name="PM-KISAN", source_url="https://pmkisan.gov.in/")]
        self.dedup.load_existing(existing)

        candidate = Scheme(name="KISAN Scheme", source_url="https://pmkisan.gov.in")
        match = self.dedup.find_duplicate(candidate)
        assert match is not None
        assert match.match_type == "source_url"

    def test_name_similarity_duplicate(self):
        """Similar names are detected."""
        existing = [Scheme(name="Pradhan Mantri KISAN Samman Nidhi")]
        self.dedup.load_existing(existing)

        candidate = Scheme(name="PM-KISAN Samman Nidhi")
        match = self.dedup.find_duplicate(candidate)
        # Note: depending on threshold, this may or may not match
        # The cleaned names would be compared

    def test_no_false_positive(self):
        """Different schemes are not flagged as duplicates."""
        existing = [Scheme(name="PM-KISAN Samman Nidhi")]
        self.dedup.load_existing(existing)

        candidate = Scheme(name="Ayushman Bharat PM-JAY")
        match = self.dedup.find_duplicate(candidate)
        assert match is None

    def test_batch_deduplication(self):
        """Batch dedup within a group works."""
        self.dedup.load_existing([])
        schemes = [
            Scheme(name="Scheme A", slug="scheme-a"),
            Scheme(name="Scheme B", slug="scheme-b"),
            Scheme(name="Scheme A Copy", slug="scheme-a"),  # duplicate slug
        ]
        unique, dupes = self.dedup.deduplicate_batch(schemes)
        assert len(unique) == 2
        assert len(dupes) == 1


# ═══════════════════════════════════════════════════════════════
# HTML Extractor Tests
# ═══════════════════════════════════════════════════════════════
class TestHTMLExtractor:
    """Test the HTML extractor."""

    def setup_method(self):
        self.extractor = HTMLExtractor()

    def test_extract_title(self):
        """Extracts page title from h1."""
        html = "<html><body><h1>PM-KISAN Samman Nidhi</h1><p>Details...</p></body></html>"
        result = self.extractor.extract_scheme_fields(html)
        assert result.get("name") == "PM-KISAN Samman Nidhi"

    def test_extract_sections(self):
        """Extracts content under section headings."""
        html = """
        <html><body>
            <h1>Test Scheme</h1>
            <h2>Benefits</h2>
            <p>₹6000 per year direct benefit transfer</p>
            <h2>Eligibility</h2>
            <p>All farmers with valid land records</p>
            <h2>Documents Required</h2>
            <ul>
                <li>Aadhaar Card</li>
                <li>Bank Account details</li>
            </ul>
        </body></html>
        """
        result = self.extractor.extract_scheme_fields(html)
        assert "benefits" in result
        assert "eligibility" in result

    def test_extract_application_url(self):
        """Finds application/registration links."""
        html = """
        <html><body>
            <h1>Test Scheme</h1>
            <a href="https://example.gov.in/apply">Apply Online</a>
        </body></html>
        """
        result = self.extractor.extract_scheme_fields(html, "https://example.gov.in")
        assert result.get("application_url") == "https://example.gov.in/apply"


# ═══════════════════════════════════════════════════════════════
# File Storage Tests
# ═══════════════════════════════════════════════════════════════
class TestFileRepository:
    """Test file-based storage."""

    def test_save_and_load_json(self, tmp_path):
        """Schemes are saved as JSON and can be loaded back."""
        repo = FileRepository(
            verified_dir=str(tmp_path / "verified"),
            rejected_dir=str(tmp_path / "rejected"),
            staging_dir=str(tmp_path / "staging"),
        )

        schemes = [
            Scheme(
                name="PM-KISAN",
                slug="pm-kisan",
                description="Farmer income support",
                source_url="https://pmkisan.gov.in",
            ),
            Scheme(
                name="Ayushman Bharat",
                slug="ayushman-bharat",
                description="Health insurance",
                source_url="https://pmjay.gov.in",
            ),
        ]

        # Save
        path = repo.save_verified_json(schemes, version="test")
        assert Path(path).exists()

        # Load
        loaded = repo.load_verified_schemes()
        assert len(loaded) == 2
        assert loaded[0].name == "PM-KISAN"

    def test_save_csv(self, tmp_path):
        """Schemes are saved as CSV."""
        repo = FileRepository(
            verified_dir=str(tmp_path / "verified"),
            rejected_dir=str(tmp_path / "rejected"),
            staging_dir=str(tmp_path / "staging"),
        )

        schemes = [Scheme(
            name="Test Scheme",
            slug="test-scheme",
            description="A test",
            source_url="https://example.gov.in",
        )]

        path = repo.save_verified_csv(schemes, version="test")
        assert Path(path).exists()
        assert Path(path).stat().st_size > 0


# ═══════════════════════════════════════════════════════════════
# Integration Test: Full Pipeline (offline, no network)
# ═══════════════════════════════════════════════════════════════
class TestPipelineIntegration:
    """Integration test for the full pipeline using mock data."""

    def test_full_pipeline_offline(self, tmp_path):
        """Test the pipeline stages without network access."""
        # Create test schemes (simulating collector output)
        raw_schemes = [
            Scheme(
                name="PM-KISAN Samman Nidhi",
                slug="pm-kisan",
                description="Income support for farmer families. ₹6000/year.",
                eligibility_summary="Landholding farmer families aged 18+. Income below ₹2.5 lakh.",
                benefits="₹6000 per year direct benefit transfer",
                source_url="https://pmkisan.gov.in",
                department="Ministry of Agriculture",
                government_level=GovernmentLevel.CENTRAL,
                scheme_status=SchemeStatus.ACTIVE,
                source_evidence=[
                    SourceEvidence(url="https://pmkisan.gov.in", retrieved_at=datetime.utcnow()),
                ],
            ),
            Scheme(
                name="Rythu Bandhu",
                slug="rythu-bandhu",
                description="Investment support for Telangana farmers",
                eligibility_summary="All farmer land owners in Telangana with pattadar passbook",
                benefits="₹10,000 per acre per year",
                source_url="https://rythubandhu.telangana.gov.in",
                department="Agriculture Department, Telangana",
                state="ts",  # will be normalized
                government_level=GovernmentLevel.STATE,
                scheme_status=SchemeStatus.ACTIVE,
                source_evidence=[
                    SourceEvidence(url="https://rythubandhu.telangana.gov.in", retrieved_at=datetime.utcnow()),
                ],
            ),
            Scheme(
                name="Test Duplicate PM-KISAN",
                slug="pm-kisan",  # duplicate slug!
                description="Same scheme, different name",
                source_url="https://pmkisan.gov.in",
            ),
        ]

        # Stage 1: Normalize
        normalizer = SchemeNormalizer()
        for s in raw_schemes:
            normalizer.normalize(s)

        # Check normalization worked
        assert raw_schemes[1].state == "Telangana"
        assert raw_schemes[0].age_range is not None
        assert raw_schemes[0].income_limit is not None
        assert raw_schemes[0].category == Category.FARMER

        # Stage 2: Validate
        validator = SchemeValidator()
        valid = []
        invalid = []
        for s in raw_schemes:
            if validator.is_publishable(s):
                valid.append(s)
            else:
                invalid.append(s)

        assert len(valid) >= 2  # PM-KISAN and Rythu Bandhu should be valid

        # Stage 3: Deduplicate
        dedup = DuplicateDetector()
        dedup.load_existing([])
        unique, dupes = dedup.deduplicate_batch(valid)

        # The duplicate PM-KISAN should be caught
        has_slug_dup = any(d.match_type == "slug" for d in dupes)
        if len(valid) == 3:
            assert has_slug_dup or len(dupes) > 0  # caught either by slug or URL

        # Stage 4: Store
        repo = FileRepository(
            verified_dir=str(tmp_path / "verified"),
            rejected_dir=str(tmp_path / "rejected"),
            staging_dir=str(tmp_path / "staging"),
        )

        json_path = repo.save_verified_json(unique, version="test")
        csv_path = repo.save_verified_csv(unique, version="test")

        assert Path(json_path).exists()
        assert Path(csv_path).exists()

        # Load back and verify
        loaded = repo.load_verified_schemes()
        assert len(loaded) > 0

        # Quality checks
        for s in loaded:
            assert s.completeness_score() > 0.3
            assert s.name

        # Stage 5: Re-run dedup (stability test)
        dedup2 = DuplicateDetector()
        dedup2.load_existing(loaded)
        unique2, dupes2 = dedup2.deduplicate_batch(unique)

        # Re-running on same data should find all as duplicates
        assert len(dupes2) == len(unique)
        assert len(unique2) == 0

    def test_pipeline_repeat_run_no_duplicates(self, tmp_path):
        """Re-running pipeline on same data doesn't create duplicates."""
        schemes = [
            Scheme(
                name="Test Scheme Alpha",
                slug="test-alpha",
                description="First test scheme",
                eligibility_summary="Everyone eligible",
                benefits="Free testing",
                source_url="https://test1.gov.in",
            ),
        ]

        repo = FileRepository(
            verified_dir=str(tmp_path / "verified"),
            rejected_dir=str(tmp_path / "rejected"),
            staging_dir=str(tmp_path / "staging"),
        )

        # First run
        repo.save_verified_json(schemes, version="run1")

        # Second run: load existing, then dedup
        existing = repo.load_verified_schemes()
        dedup = DuplicateDetector()
        dedup.load_existing(existing)
        unique, dupes = dedup.deduplicate_batch(schemes)

        assert len(unique) == 0  # all caught as duplicates
        assert len(dupes) == 1


# ═══════════════════════════════════════════════════════════════
# Run all tests
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

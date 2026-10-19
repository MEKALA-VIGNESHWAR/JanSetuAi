"""
JanSetuAI — Telangana Government Portal Collector
===================================================
Collects scheme data from Telangana state government portals.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

from data_pipeline.sources.base_collector import BaseCollector
from data_pipeline.validation.schema import (
    AgeRange,
    BenefitType,
    Category,
    GovernmentLevel,
    OpportunityType,
    Scheme,
    SchemeStatus,
    SourceEvidence,
    VerificationStatus,
)

logger = logging.getLogger(__name__)

# Known Telangana government scheme URLs and their departments
TELANGANA_SCHEME_REGISTRY = [
    {
        "name": "Rythu Bandhu",
        "url": "https://rythubandhu.telangana.gov.in/",
        "department": "Agriculture Department, Telangana",
        "category": Category.FARMER,
        "benefit_type": BenefitType.FINANCIAL,
        "benefit_amount": "₹10,000/acre/year",
        "description": "Investment support of ₹10,000 per acre per year for farmer land owners for crop production, paid in two installments.",
        "eligibility": "All farmer land owners in Telangana with pattadar passbook. No income ceiling.",
        "documents": ["Aadhaar Card", "Pattadar Passbook", "Bank Account (linked to Aadhaar)"],
        "application_url": "https://rythubandhu.telangana.gov.in/",
    },
    {
        "name": "Rythu Bima",
        "url": "https://rythubandhu.telangana.gov.in/Default_RB1.aspx",
        "department": "Agriculture Department, Telangana",
        "category": Category.FARMER,
        "benefit_type": BenefitType.INSURANCE,
        "benefit_amount": "₹5,00,000 life insurance",
        "description": "Free life insurance of ₹5 lakh for all farmer pattadars aged 18-59. Premium paid by state government.",
        "eligibility": "Farmer pattadars in Telangana aged 18-59 years.",
        "documents": ["Aadhaar Card", "Pattadar Passbook", "Age Proof", "Bank Account", "Nominee Details"],
        "application_url": "https://rythubandhu.telangana.gov.in/Default_RB1.aspx",
        "age_min": 18,
        "age_max": 59,
    },
    {
        "name": "Telangana ePASS Scholarship",
        "url": "https://telanganaepass.cgg.gov.in/",
        "department": "Backward Classes Welfare, Telangana",
        "category": Category.STUDENT,
        "benefit_type": BenefitType.SCHOLARSHIP,
        "description": "Post-matric scholarship and tuition fee reimbursement for SC/ST/BC/EBC/Minority students in Telangana.",
        "eligibility": "SC/ST/BC/EBC/Minority students from Telangana. Family income below ₹2 lakh.",
        "documents": ["Aadhaar Card", "Income Certificate", "Caste Certificate", "College Admission Letter", "Previous Marksheets", "Bank Account"],
        "application_url": "https://telanganaepass.cgg.gov.in/",
    },
    {
        "name": "Kalyana Lakshmi / Shaadi Mubarak",
        "url": "https://kalyanamasthu.cgg.gov.in/",
        "department": "Women Development & Child Welfare, Telangana",
        "category": Category.WOMEN,
        "benefit_type": BenefitType.FINANCIAL,
        "benefit_amount": "₹1,00,116",
        "description": "Financial assistance of ₹1,00,116 at the time of marriage for women from SC/ST/BC/Minority/EBC families.",
        "eligibility": "Woman aged 18+ from Telangana belonging to SC/ST/BC/Minority/EBC. Family income below ₹2 lakh.",
        "documents": ["Aadhaar Card", "Caste Certificate", "Income Certificate", "Age Proof", "Bank Account", "Marriage Invitation/Proof"],
        "application_url": "https://kalyanamasthu.cgg.gov.in/",
    },
    {
        "name": "Aasara Pension Scheme",
        "url": "https://www.telangana.gov.in/",
        "department": "Panchayat Raj & Rural Development, Telangana",
        "category": Category.SENIOR_CITIZEN,
        "benefit_type": BenefitType.FINANCIAL,
        "benefit_amount": "₹2,016/month",
        "description": "Monthly pension for old age (65+), widows, disabled persons, weavers, toddy tappers, single women, and beedi workers.",
        "eligibility": "Telangana resident meeting category-specific criteria: 65+ for old age pension, widows, PwD (40%+), etc.",
        "documents": ["Aadhaar Card", "Age Proof", "Residence Certificate", "Category-specific Certificate", "Bank Account"],
    },
    {
        "name": "Dalit Bandhu",
        "url": "https://dalitbandhu.telangana.gov.in/",
        "department": "SC Development Department, Telangana",
        "category": Category.GENERAL,
        "benefit_type": BenefitType.FINANCIAL,
        "benefit_amount": "₹10,00,000",
        "description": "Direct benefit of ₹10 lakh per SC family for setting up enterprises. 100% grant, no repayment required.",
        "eligibility": "Scheduled Caste (Dalit) families in Telangana, selected constituency-wise.",
        "documents": ["Aadhaar Card", "Caste Certificate (SC)", "Bank Account", "Residence Proof", "Business Plan"],
        "application_url": "https://dalitbandhu.telangana.gov.in/",
    },
    {
        "name": "T-Hub Startup Incubation",
        "url": "https://t-hub.co/",
        "department": "IT & Industries Department, Telangana",
        "category": Category.ENTREPRENEUR,
        "benefit_type": BenefitType.SERVICE,
        "description": "Startup incubation, mentoring, investor connect, and workspace for technology startups in Telangana.",
        "eligibility": "Registered startup/entrepreneur. Preferably based in Hyderabad/Telangana.",
        "documents": ["Company Registration", "Business Plan", "Founder Aadhaar/PAN", "Bank Account"],
        "application_url": "https://t-hub.co/programs/",
    },
    {
        "name": "WE Hub — Women Entrepreneurship",
        "url": "https://wehub.telangana.gov.in/",
        "department": "WE Hub, Government of Telangana",
        "category": Category.WOMEN,
        "benefit_type": BenefitType.SERVICE,
        "description": "India's first state-led incubator for women entrepreneurs. Provides mentoring, funding connect, and workspace.",
        "eligibility": "Women entrepreneurs and women-led startups. Preferably from Telangana.",
        "documents": ["Aadhaar Card", "Company Registration", "Business Plan"],
        "application_url": "https://wehub.telangana.gov.in/",
    },
    {
        "name": "Telangana Skill Development Programme",
        "url": "https://tsdcl.telangana.gov.in/",
        "department": "Labour, Employment & Training Department, Telangana",
        "category": Category.JOB_SEEKER,
        "benefit_type": BenefitType.TRAINING,
        "description": "Free skill training programs across various sectors for youth in Telangana, with placement assistance.",
        "eligibility": "Youth aged 15-35 from Telangana. No minimum education for many courses.",
        "documents": ["Aadhaar Card", "Age Proof", "Residence Proof", "Education Certificates", "Bank Account"],
        "application_url": "https://tsdcl.telangana.gov.in/",
        "age_min": 15,
        "age_max": 35,
    },
    {
        "name": "CM Overseas Scholarship for BC/EBC/Minorities",
        "url": "https://overseas.tsobmms.com/",
        "department": "Backward Classes Welfare, Telangana",
        "category": Category.STUDENT,
        "benefit_type": BenefitType.SCHOLARSHIP,
        "description": "Full scholarship for BC/EBC/Minority students from Telangana to pursue postgraduate studies abroad.",
        "eligibility": "BC/EBC/Minority student from Telangana. Family income below ₹5 lakh. Admission in foreign university.",
        "documents": ["Aadhaar Card", "Caste Certificate", "Income Certificate", "Admission Letter", "Passport", "Academic Transcripts"],
        "application_url": "https://overseas.tsobmms.com/",
    },
]


class TelanganaCollector(BaseCollector):
    """
    Collects Telangana state government scheme data.
    Uses a curated registry + HTML scraping for enrichment.
    """

    def __init__(self, raw_data_dir: str = "data/raw"):
        super().__init__(
            source_name="telangana",
            base_url="https://www.telangana.gov.in",
            raw_data_dir=raw_data_dir,
            request_delay=2.0,
        )

    def discover(self) -> list[dict[str, Any]]:
        """Return known Telangana scheme entries."""
        entries = []
        for reg in TELANGANA_SCHEME_REGISTRY:
            entries.append({
                "url": reg["url"],
                "name": reg["name"],
                "registry": reg,
            })
        return entries

    def extract_scheme(self, entry: dict[str, Any]) -> Scheme | None:
        """Extract and build scheme from registry + optional HTML enrichment."""
        reg = entry["registry"]
        url = entry["url"]

        # Try to fetch the actual page for evidence
        snapshot = None
        try:
            resp = self.fetch_url(url)
            snapshot = self.save_raw_snapshot(
                url=url,
                content=resp.text,
                content_type="html",
                http_status=resp.status_code,
            )
        except Exception as e:
            logger.warning(f"Could not fetch {url}: {e}")

        # Build age range if specified
        age_range = None
        if reg.get("age_min") or reg.get("age_max"):
            age_range = AgeRange(
                min_age=reg.get("age_min"),
                max_age=reg.get("age_max"),
            )

        evidence = [
            SourceEvidence(
                url=url,
                retrieved_at=datetime.utcnow(),
                snapshot_path=snapshot.raw_file_path if snapshot else None,
            )
        ]

        return Scheme(
            name=reg["name"],
            description=reg.get("description", ""),
            opportunity_type=OpportunityType.SCHEME,
            category=reg.get("category", Category.GENERAL),
            government_level=GovernmentLevel.STATE,
            state="Telangana",
            scheme_status=SchemeStatus.ACTIVE,
            benefits=reg.get("description", ""),
            benefit_type=reg.get("benefit_type", BenefitType.OTHER),
            benefit_amount=reg.get("benefit_amount", ""),
            eligibility_summary=reg.get("eligibility", ""),
            required_documents=reg.get("documents", []),
            application_url=reg.get("application_url", ""),
            department=reg.get("department", ""),
            official_source=reg.get("department", "Government of Telangana"),
            source_url=url,
            age_range=age_range,
            verification_status=VerificationStatus.PENDING,
            source_evidence=evidence,
        )

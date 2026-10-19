"""
JanSetuAI — Central Ministry Portal Collector
============================================
Collects scheme data from central government ministry websites.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Optional

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

# Known central ministry scheme URLs and their departments
CENTRAL_SCHEME_REGISTRY = [
    {
        "name": "PM-KISAN Samman Nidhi",
        "url": "https://pmkisan.gov.in/",
        "department": "Ministry of Agriculture & Farmers Welfare",
        "category": Category.FARMER,
        "benefit_type": BenefitType.FINANCIAL,
        "benefit_amount": "₹6,000/year (3 installments)",
        "description": "Direct income support of ₹6,000/year to farmer families in three equal installments of ₹2,000 each.",
        "eligibility": "All landholding farmer families with cultivable land. Excludes institutional landholders, government employees, income tax payers, and professionals.",
        "documents": ["Aadhaar Card", "Bank Account linked to Aadhaar", "Land Ownership Records", "State Revenue Records"],
        "application_url": "https://pmkisan.gov.in/",
        "age_min": 18,
    },
    {
        "name": "PM Fasal Bima Yojana",
        "url": "https://pmfby.gov.in/",
        "department": "Ministry of Agriculture & Farmers Welfare",
        "category": Category.FARMER,
        "benefit_type": BenefitType.INSURANCE,
        "description": "Crop insurance at affordable premiums for farmers against natural calamities, pests, and diseases.",
        "eligibility": "All farmers including sharecroppers and tenant farmers growing notified crops in notified areas.",
        "documents": ["Aadhaar Card", "Bank Account", "Land Records/Lease Agreement", "Sowing Certificate", "Crop Details"],
        "application_url": "https://pmfby.gov.in/",
        "age_min": 18,
    },
    {
        "name": "Kisan Credit Card",
        "url": "https://www.pmkisan.gov.in/KCC",
        "department": "Ministry of Agriculture & Farmers Welfare",
        "category": Category.FARMER,
        "benefit_type": BenefitType.LOAN,
        "description": "Affordable agricultural credit for farmers for their agricultural needs including crop production, post-harvest expenses, and maintenance of farm assets.",
        "eligibility": "All farmers including individual/joint borrowers, tenant farmers, oral lessees, sharecroppers, self-help groups, and joint liability groups.",
        "documents": ["Aadhaar Card", "PAN Card", "Land Records", "Passport-size Photos", "Application Form", "Bank Account Details"],
        "application_url": "https://www.pmkisan.gov.in/KCC",
        "age_min": 18,
        "age_max": 75,
    },
    {
        "name": "Ayushman Bharat PM-JAY",
        "url": "https://pmjay.gov.in/",
        "department": "Ministry of Health & Family Welfare",
        "category": Category.GENERAL,
        "benefit_type": BenefitType.INSURANCE,
        "benefit_amount": "₹5,00,000/year",
        "description": "Health insurance cover of ₹5 lakh per family per year for secondary and tertiary hospitalization.",
        "eligibility": "Families identified in SECC 2011 database (rural deprivation, urban occupation criteria). Recently extended to all citizens aged 70+ regardless of income.",
        "documents": ["Aadhaar Card", "Ration Card", "SECC Data Match", "Mobile Number"],
        "application_url": "https://pmjay.gov.in/",
    },
    {
        "name": "PM Awas Yojana",
        "url": "https://pmaymis.gov.in/",
        "department": "Ministry of Housing & Urban Affairs",
        "category": Category.GENERAL,
        "benefit_type": BenefitType.HOUSING,
        "description": "Affordable housing to urban and rural poor through interest subsidy on home loans and direct construction assistance.",
        "eligibility": "EWS (income ≤₹3 lakh), LIG (₹3-6 lakh), MIG-I (₹6-12 lakh), MIG-II (₹12-18 lakh). Must not own a pucca house in India.",
        "documents": ["Aadhaar Card", "Income Certificate", "Bank Account", "Land Records / NOC", "No-property Certificate"],
        "application_url": "https://pmaymis.gov.in/",
        "age_min": 18,
    },
    {
        "name": "PM SVANidhi",
        "url": "https://pmsvanidhi.mohua.gov.in/",
        "department": "Ministry of Housing & Urban Affairs",
        "category": Category.JOB_SEEKER,
        "benefit_type": BenefitType.LOAN,
        "benefit_amount": "₹10,000-50,000",
        "description": "Working capital loan for street vendors with interest subsidy.",
        "eligibility": "Street vendors with Certificate of Vending or Letter of Recommendation from ULB. Must have been vending before/during COVID period.",
        "documents": ["Certificate of Vending / LoR from ULB", "Aadhaar Card", "Bank Account", "Passport-size Photo", "Vending location details"],
        "application_url": "https://pmsvanidhi.mohua.gov.in/",
        "age_min": 18,
    },
    {
        "name": "PM Ujjwala Yojana",
        "url": "https://www.pmujjwalayojana.com/",
        "department": "Ministry of Petroleum & Natural Gas",
        "category": Category.WOMEN,
        "benefit_type": BenefitType.SUBSIDY,
        "description": "Free LPG connection with ₹1,600 financial support for gas stove and first refill for women from BPL households.",
        "eligibility": "Women from BPL households, SC/ST, beneficiaries of PMAY/AAY/forest dwellers/most backward classes/tea garden workers/river island residents.",
        "documents": ["Aadhaar Card", "BPL Ration Card / Category Proof", "Bank Account", "Passport-size Photo", "Address Proof"],
        "application_url": "https://www.pmujjwalayojana.com/",
        "age_min": 18,
        "gender_restriction": "FEMALE",
    },
    {
        "name": "PM Mudra Yojana",
        "url": "https://www.mudra.org.in/",
        "department": "Ministry of Finance / MUDRA",
        "category": Category.ENTREPRENEUR,
        "benefit_type": BenefitType.LOAN,
        "description": "Collateral-free business loans up to ₹20 lakh for micro/small enterprises.",
        "eligibility": "Any Indian citizen with business plan for non-farm income generating activities. No collateral needed. Both new and existing businesses eligible.",
        "documents": ["Aadhaar Card", "PAN Card", "Business Plan/Proposal", "Bank Account", "Address Proof", "Business Registration (if existing)"],
        "application_url": "https://www.mudra.org.in/",
        "age_min": 18,
    },
    {
        "name": "Startup India",
        "url": "https://www.startupindia.gov.in/",
        "department": "Ministry of Commerce & Industry (DPIIT)",
        "category": Category.ENTREPRENEUR,
        "benefit_type": BenefitType.SUBSIDY,
        "description": "Tax benefits, funding support, compliance simplifications, and mentorship for registered startups.",
        "eligibility": "Entity incorporated as Private Limited/LLP/Partnership. Less than 10 years old. Annual turnover below ₹100 crore. Working toward innovation/development.",
        "documents": ["Certificate of Incorporation", "PAN Card of Entity", "DPIIT Recognition Certificate", "Pitch Deck / Innovation Description"],
        "application_url": "https://www.startupindia.gov.in/",
        "age_min": 18,
    },
    {
        "name": "Stand-Up India",
        "url": "https://www.standupmitra.in/",
        "department": "Ministry of Finance / Department of Financial Services",
        "category": Category.ENTREPRENEUR,
        "benefit_type": BenefitType.LOAN,
        "description": "Bank loans between ₹10 lakh and ₹1 crore for SC/ST and women entrepreneurs for greenfield enterprises.",
        "eligibility": "SC/ST and/or women entrepreneur(s) above 18. For greenfield (new) enterprise only. At least 51% shareholding by SC/ST/women. Should not be in default.",
        "documents": ["SC/ST Caste Certificate or Gender Proof", "Aadhaar Card", "PAN Card", "Business Plan", "Bank Account", "Address Proof", "IT Returns (if any)"],
        "application_url": "https://www.standupmitra.in/",
        "age_min": 18,
    },
]


class CentralPortalsCollector(BaseCollector):
    """
    Collects schemes from central government ministry portals.
    Uses a curated registry of known central schemes.
    """

    def __init__(self, raw_data_dir: str = "data/raw"):
        super().__init__(
            source_name="central_portals",
            base_url="https://www.myscheme.gov.in",
            raw_data_dir=raw_data_dir,
            request_delay=1.5,
        )

    def discover(self) -> list[dict[str, Any]]:
        """Return known central scheme entries."""
        entries = []
        for reg in CENTRAL_SCHEME_REGISTRY:
            entries.append({
                "url": reg["url"],
                "name": reg["name"],
                "registry": reg,
            })
        return entries

    def extract_scheme(self, entry: dict[str, Any]) -> Scheme | None:
        """Extract and build scheme from registry."""
        reg = entry["registry"]
        url = entry["url"]
        name = reg.get("name", "Unknown")

        # Try to fetch the actual page for evidence
        snapshot = None
        try:
            resp = self.fetch_url(url)
            snapshot = self.save_raw_snapshot(
                url=url,
                content=resp.text,
                content_type="html",
                http_status=resp.status_code,
                extra_name=reg.get("slug", name.lower().replace(" ", "-")),
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

        gender_restriction = None
        if reg.get("gender_restriction"):
            gender_restriction = reg.get("gender_restriction")

        return Scheme(
            name=reg["name"],
            description=reg.get("description", ""),
            opportunity_type=OpportunityType.SCHEME,
            category=reg.get("category", Category.GENERAL),
            government_level=GovernmentLevel.CENTRAL,
            state=None,  # Central schemes apply nationwide
            scheme_status=SchemeStatus.ACTIVE,
            benefits=reg.get("description", ""),
            benefit_type=reg.get("benefit_type", BenefitType.OTHER),
            benefit_amount=reg.get("benefit_amount", ""),
            eligibility_summary=reg.get("eligibility", ""),
            required_documents=reg.get("documents", []),
            application_url=reg.get("application_url", ""),
            department=reg.get("department", ""),
            official_source=reg.get("department", "Government of India"),
            source_url=url,
            age_range=age_range,
            gender_restriction=gender_restriction,
            application_mode=self._detect_application_mode(reg),
            verification_status=VerificationStatus.PENDING,
            source_evidence=[
                SourceEvidence(
                    url=url,
                    retrieved_at=datetime.utcnow(),
                    snapshot_path=snapshot.raw_file_path if snapshot else None,
                )
            ],
        )

    def _detect_application_mode(self, reg: dict) -> str:
        """Detect application mode from URL and description."""
        url = reg.get("url", "").lower()
        if ".gov.in" in url or "portal" in url:
            return "ONLINE"
        # Check if online portal mentioned
        desc = (reg.get("description", "") + " " + reg.get("url", "")).lower()
        if "visit" in desc and "bank" in desc:
            return "BOTH"
        if "visit" in desc or "nearest" in desc:
            return "OFFLINE"
        return "ONLINE"
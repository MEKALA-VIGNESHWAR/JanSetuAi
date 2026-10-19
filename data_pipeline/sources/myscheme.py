"""
JanSetuAI — myScheme.gov.in Collector
======================================
Collects scheme data from the myScheme portal API.
myScheme provides a JSON API that lists central and state schemes
with eligibility, benefits, and application details.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Optional

from data_pipeline.sources.base_collector import BaseCollector
from data_pipeline.validation.schema import (
    AgeRange,
    ApplicationMode,
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

# Mapping from myScheme categories to our canonical categories
CATEGORY_MAP = {
    "agriculture": Category.FARMER,
    "farmer": Category.FARMER,
    "education": Category.STUDENT,
    "student": Category.STUDENT,
    "scholarship": Category.STUDENT,
    "employment": Category.JOB_SEEKER,
    "skill": Category.JOB_SEEKER,
    "women": Category.WOMEN,
    "girl": Category.WOMEN,
    "business": Category.ENTREPRENEUR,
    "entrepreneur": Category.ENTREPRENEUR,
    "startup": Category.ENTREPRENEUR,
    "senior": Category.SENIOR_CITIZEN,
    "pension": Category.SENIOR_CITIZEN,
    "minority": Category.MINORITY,
}

BENEFIT_TYPE_MAP = {
    "financial assistance": BenefitType.FINANCIAL,
    "scholarship": BenefitType.SCHOLARSHIP,
    "subsidy": BenefitType.SUBSIDY,
    "loan": BenefitType.LOAN,
    "insurance": BenefitType.INSURANCE,
    "training": BenefitType.TRAINING,
    "employment": BenefitType.JOB,
    "housing": BenefitType.HOUSING,
}


class MySchemeCollector(BaseCollector):
    """
    Collects schemes from myScheme.gov.in.
    
    Strategy:
    1. Use the public search/listing endpoints to discover schemes
    2. Fetch individual scheme details
    3. Extract structured fields
    """

    def __init__(self, raw_data_dir: str = "data/raw", max_schemes: int = 50):
        super().__init__(
            source_name="myscheme",
            base_url="https://www.myscheme.gov.in",
            raw_data_dir=raw_data_dir,
            request_delay=2.0,  # be respectful
        )
        self.max_schemes = max_schemes
        self.api_base = f"{self.base_url}/api"

    def discover(self) -> list[dict[str, Any]]:
        """
        Discover schemes from myScheme portal.
        First tries the API, falls back to known scheme slugs for pilot.
        """
        entries = []

        # Attempt API discovery
        try:
            entries = self._discover_via_api()
            if entries:
                return entries[:self.max_schemes]
        except Exception as e:
            logger.warning(f"API discovery failed: {e}, falling back to known schemes")

        # Fallback: known pilot scheme URLs for the initial 25-scheme pilot
        entries = self._get_pilot_schemes()
        return entries[:self.max_schemes]

    def _discover_via_api(self) -> list[dict[str, Any]]:
        """Try to discover schemes via myScheme's search/listing API."""
        entries = []

        # myScheme has a search API — try paginated listing
        search_urls = [
            f"{self.api_base}/search?q=&limit=25&offset=0",
            f"{self.base_url}/api/v1/schemes?limit=25",
            f"{self.base_url}/search/api/schemes",
        ]

        for url in search_urls:
            try:
                response = self.fetch_url(url)
                data = response.json()

                # Save raw response
                self.save_raw_snapshot(
                    url=url,
                    content=json.dumps(data, indent=2, ensure_ascii=False),
                    content_type="json",
                    http_status=response.status_code,
                )

                # Parse based on response structure
                schemes_list = []
                if isinstance(data, list):
                    schemes_list = data
                elif isinstance(data, dict):
                    schemes_list = data.get("data", data.get("schemes", data.get("results", [])))

                for item in schemes_list:
                    slug = item.get("slug", item.get("id", ""))
                    name = item.get("name", item.get("title", item.get("schemeName", "")))
                    if slug or name:
                        entries.append({
                            "url": f"{self.base_url}/schemes/{slug}" if slug else "",
                            "slug": slug,
                            "name": name,
                            "raw_data": item,
                        })

                if entries:
                    logger.info(f"Discovered {len(entries)} schemes via API: {url}")
                    return entries

            except Exception as e:
                logger.debug(f"API endpoint {url} failed: {e}")
                continue

        return entries

    def _get_pilot_schemes(self) -> list[dict[str, Any]]:
        """
        Known pilot schemes for initial pipeline testing.
        These are real schemes on myScheme.gov.in with known slugs.
        """
        pilot_schemes = [
            # Central — Farmer schemes
            {"slug": "pradhan-mantri-kisan-samman-nidhi", "name": "PM-KISAN Samman Nidhi", "category": "farmer"},
            {"slug": "pradhan-mantri-fasal-bima-yojana", "name": "PM Fasal Bima Yojana", "category": "farmer"},
            {"slug": "kisan-credit-card-kcc", "name": "Kisan Credit Card", "category": "farmer"},
            {"slug": "pradhan-mantri-krishi-sinchai-yojana", "name": "PM Krishi Sinchai Yojana", "category": "farmer"},
            {"slug": "pradhan-mantri-kisan-maandhan-yojana", "name": "PM Kisan MaanDhan Yojana", "category": "farmer"},

            # Central — Student schemes
            {"slug": "central-sector-scheme-of-scholarships", "name": "Central Sector Scheme of Scholarships", "category": "student"},
            {"slug": "post-matric-scholarship-for-sc-students", "name": "Post Matric Scholarship for SC Students", "category": "student"},
            {"slug": "post-matric-scholarship-for-st-students", "name": "Post Matric Scholarship for ST Students", "category": "student"},
            {"slug": "pragati-scholarship-scheme-for-girls", "name": "Pragati Scholarship for Girls", "category": "student"},
            {"slug": "pm-vidyalaxmi", "name": "PM Vidyalaxmi", "category": "student"},

            # Central — Job Seeker / General
            {"slug": "pradhan-mantri-kaushal-vikas-yojana", "name": "PM Kaushal Vikas Yojana", "category": "employment"},
            {"slug": "mahatma-gandhi-nrega", "name": "Mahatma Gandhi NREGA", "category": "employment"},
            {"slug": "pradhan-mantri-mudra-yojana", "name": "PM Mudra Yojana", "category": "business"},
            {"slug": "startup-india", "name": "Startup India", "category": "business"},
            {"slug": "ayushman-bharat-pm-jay", "name": "Ayushman Bharat PM-JAY", "category": "general"},

            # Central — Women
            {"slug": "pradhan-mantri-matru-vandana-yojana", "name": "PM Matru Vandana Yojana", "category": "women"},
            {"slug": "sukanya-samriddhi-yojana", "name": "Sukanya Samriddhi Yojana", "category": "women"},
            {"slug": "pradhan-mantri-ujjwala-yojana", "name": "PM Ujjwala Yojana", "category": "women"},

            # Telangana specific
            {"slug": "rythu-bandhu", "name": "Rythu Bandhu", "category": "farmer", "state": "Telangana"},
            {"slug": "rythu-bima", "name": "Rythu Bima", "category": "farmer", "state": "Telangana"},
            {"slug": "telangana-epass", "name": "Telangana ePASS", "category": "student", "state": "Telangana"},
            {"slug": "kalyana-lakshmi", "name": "Kalyana Lakshmi / Shaadi Mubarak", "category": "women", "state": "Telangana"},
            {"slug": "aasara-pension-scheme", "name": "Aasara Pensions", "category": "senior", "state": "Telangana"},
            {"slug": "dalit-bandhu", "name": "Dalit Bandhu", "category": "general", "state": "Telangana"},
            {"slug": "telangana-skill-development", "name": "Telangana Skill Development", "category": "employment", "state": "Telangana"},
        ]

        entries = []
        for ps in pilot_schemes:
            entries.append({
                "url": f"{self.base_url}/schemes/{ps['slug']}",
                "slug": ps["slug"],
                "name": ps["name"],
                "category": ps.get("category", "general"),
                "state": ps.get("state"),
                "raw_data": ps,
            })

        return entries

    def extract_scheme(self, entry: dict[str, Any]) -> Scheme | None:
        """
        Fetch and extract a single scheme from myScheme.
        Tries the API detail endpoint first, falls back to HTML scraping.
        """
        slug = entry.get("slug", "")
        name = entry.get("name", "Unknown")

        # Try API detail endpoint
        scheme_data = self._try_api_detail(slug)

        if scheme_data:
            return self._build_scheme_from_api(scheme_data, entry)

        # Try HTML page
        try:
            scheme = self._extract_from_html(entry)
            if scheme:
                return scheme
        except Exception as e:
            logger.error(f"Failed to extract {name} from HTML: {e}")

        # Fallback: build a minimal record from known pilot data
        return self._build_minimal_scheme(entry)

    def _try_api_detail(self, slug: str) -> dict | None:
        """Try to get scheme details from API."""
        detail_urls = [
            f"{self.api_base}/schemes/{slug}",
            f"{self.api_base}/v1/schemes/{slug}",
        ]
        for url in detail_urls:
            try:
                resp = self.fetch_url(url)
                data = resp.json()
                self.save_raw_snapshot(
                    url=url,
                    content=json.dumps(data, indent=2, ensure_ascii=False),
                    content_type="json",
                    http_status=resp.status_code,
                    extra_name=slug,
                )
                return data if isinstance(data, dict) else None
            except Exception:
                continue
        return None

    def _extract_from_html(self, entry: dict[str, Any]) -> Scheme | None:
        """Extract scheme info from the HTML page."""
        url = entry["url"]
        try:
            resp = self.fetch_url(url)
            html = resp.text

            self.save_raw_snapshot(
                url=url,
                content=html,
                content_type="html",
                http_status=resp.status_code,
                extra_name=entry.get("slug", ""),
            )

            # Parse with our HTML extractor (imported here to avoid circular)
            from data_pipeline.extractors.html_extractor import HTMLExtractor
            extractor = HTMLExtractor()
            extracted = extractor.extract_scheme_fields(html, url)

            # Only treat extraction as successful if meaningful name/content found.
            # myScheme.gov.in is JS-rendered; HTML extraction often yields empty values.
            if extracted and extracted.get("name", "").strip():
                return self._build_scheme_from_extracted(extracted, entry)

        except Exception as e:
            logger.warning(f"HTML extraction failed for {url}: {e}")

        return None

    def _build_scheme_from_api(self, data: dict, entry: dict) -> Scheme:
        """Build a Scheme object from API response data."""
        cat_str = entry.get("category", "general").lower()
        category = CATEGORY_MAP.get(cat_str, Category.GENERAL)

        # Detect benefit type
        benefit_type = BenefitType.OTHER
        benefits_text = str(data.get("benefits", "") or data.get("benefit", "")).lower()
        for key, bt in BENEFIT_TYPE_MAP.items():
            if key in benefits_text:
                benefit_type = bt
                break

        # Detect government level
        state = entry.get("state") or data.get("state")
        gov_level = GovernmentLevel.STATE if state else GovernmentLevel.CENTRAL

        return Scheme(
            name=data.get("name", data.get("title", entry["name"])),
            slug=entry.get("slug"),
            description=data.get("description", data.get("details", "")),
            short_description=data.get("shortDescription", data.get("summary", "")),
            opportunity_type=OpportunityType.SCHEME,
            category=category,
            government_level=gov_level,
            state=state,
            scheme_status=SchemeStatus.ACTIVE,
            benefits=data.get("benefits", data.get("benefit", "")),
            benefit_type=benefit_type,
            benefit_amount=data.get("benefitAmount", ""),
            eligibility_summary=data.get("eligibility", data.get("eligibilityCriteria", "")),
            required_documents=data.get("documents", data.get("requiredDocuments", [])),
            application_url=data.get("applicationUrl", data.get("applyLink", "")),
            application_steps=data.get("applicationProcess", data.get("howToApply", [])),
            department=data.get("ministry", data.get("department", "")),
            official_source=data.get("source", data.get("ministry", "")),
            source_url=entry["url"],
            verification_status=VerificationStatus.PENDING,
            source_evidence=[
                SourceEvidence(
                    url=entry["url"],
                    retrieved_at=datetime.utcnow(),
                )
            ],
        )

    def _build_scheme_from_extracted(self, extracted: dict, entry: dict) -> Scheme:
        """Build Scheme from HTML-extracted fields."""
        cat_str = entry.get("category", "general").lower()
        category = CATEGORY_MAP.get(cat_str, Category.GENERAL)
        state = entry.get("state")
        gov_level = GovernmentLevel.STATE if state else GovernmentLevel.CENTRAL

        return Scheme(
            name=extracted.get("name", entry["name"]),
            slug=entry.get("slug"),
            description=extracted.get("description", ""),
            short_description=extracted.get("short_description", ""),
            opportunity_type=OpportunityType.SCHEME,
            category=category,
            government_level=gov_level,
            state=state,
            scheme_status=SchemeStatus.ACTIVE,
            benefits=extracted.get("benefits", ""),
            eligibility_summary=extracted.get("eligibility", ""),
            required_documents=extracted.get("documents", []),
            application_url=extracted.get("application_url", ""),
            department=extracted.get("department", ""),
            source_url=entry["url"],
            verification_status=VerificationStatus.PENDING,
            source_evidence=[
                SourceEvidence(
                    url=entry["url"],
                    retrieved_at=datetime.utcnow(),
                )
            ],
        )

    def _build_minimal_scheme(self, entry: dict) -> Scheme:
        """Build a minimal scheme from known pilot data."""
        cat_str = entry.get("category", "general").lower()
        category = CATEGORY_MAP.get(cat_str, Category.GENERAL)
        state = entry.get("state")
        gov_level = GovernmentLevel.STATE if state else GovernmentLevel.CENTRAL

        return Scheme(
            name=entry["name"],
            slug=entry.get("slug"),
            opportunity_type=OpportunityType.SCHEME,
            category=category,
            government_level=gov_level,
            state=state,
            scheme_status=SchemeStatus.UNKNOWN,
            source_url=entry.get("url", ""),
            verification_status=VerificationStatus.PENDING,
            source_evidence=[
                SourceEvidence(
                    url=entry.get("url", ""),
                    retrieved_at=datetime.utcnow(),
                    relevant_text=f"Pilot scheme entry: {entry['name']}",
                )
            ],
        )

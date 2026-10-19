"""
JanSetuAI — Scheme Normalizer
================================
Converts raw extracted data into the canonical Scheme structure.
Normalizes dates, locations, eligibility, benefits, and amounts.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Optional

from data_pipeline.validation.schema import (
    AgeRange,
    ApplicationMode,
    BenefitType,
    Category,
    EligibilityRule,
    GovernmentLevel,
    IncomeLimit,
    OpportunityType,
    Scheme,
    SchemeStatus,
)

logger = logging.getLogger(__name__)


# ── Indian state normalization ──────────────────────────────────
INDIAN_STATES = {
    "andhra pradesh", "arunachal pradesh", "assam", "bihar",
    "chhattisgarh", "goa", "gujarat", "haryana", "himachal pradesh",
    "jharkhand", "karnataka", "kerala", "madhya pradesh",
    "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland",
    "odisha", "punjab", "rajasthan", "sikkim", "tamil nadu",
    "telangana", "tripura", "uttar pradesh", "uttarakhand",
    "west bengal", "delhi", "jammu and kashmir", "ladakh",
    "chandigarh", "puducherry", "lakshadweep",
    "dadra and nagar haveli and daman and diu", "andaman and nicobar islands",
}

# State name normalization map (common variants)
STATE_NORMALIZE = {
    "ap": "Andhra Pradesh",
    "ts": "Telangana",
    "tn": "Tamil Nadu",
    "mh": "Maharashtra",
    "ka": "Karnataka",
    "up": "Uttar Pradesh",
    "mp": "Madhya Pradesh",
    "wb": "West Bengal",
    "hp": "Himachal Pradesh",
    "j&k": "Jammu and Kashmir",
    "uk": "Uttarakhand",
    "jk": "Jammu and Kashmir",
    "orissa": "Odisha",
}


class SchemeNormalizer:
    """
    Normalizes extracted scheme data into canonical format.
    """

    def normalize(self, scheme: Scheme) -> Scheme:
        """
        Apply all normalization steps to a Scheme.
        Returns the same object, mutated.
        """
        self._normalize_state(scheme)
        self._normalize_districts(scheme)
        self._normalize_age_range(scheme)
        self._normalize_income_limit(scheme)
        self._normalize_benefit_type(scheme)
        self._normalize_application_mode(scheme)
        self._normalize_category(scheme)
        self._normalize_documents(scheme)
        self._normalize_tags(scheme)
        self._extract_eligibility_rules(scheme)
        self._normalize_exclusions(scheme)
        return scheme

    def _normalize_state(self, scheme: Scheme):
        """Normalize state name to proper case."""
        if not scheme.state:
            return
        state = scheme.state.strip().lower()

        # Check abbreviation map
        if state in STATE_NORMALIZE:
            scheme.state = STATE_NORMALIZE[state]
            return

        # Check full names
        for s in INDIAN_STATES:
            if s == state:
                scheme.state = s.title()
                return

        # Already proper case or unknown — leave as-is
        scheme.state = scheme.state.strip().title()

    def _normalize_districts(self, scheme: Scheme):
        """Clean district names."""
        if not scheme.districts:
            return
        cleaned = []
        for d in scheme.districts:
            d = d.strip()
            if d and d.lower() not in ("all", "na", "n/a", "all districts"):
                cleaned.append(d.title())
        scheme.districts = cleaned

    def _normalize_age_range(self, scheme: Scheme):
        """Extract age range from eligibility text if not already set."""
        if scheme.age_range:
            return

        text = (scheme.eligibility_summary or "") + " " + (scheme.description or "")
        if not text.strip():
            return

        # Patterns: "aged 18-40", "18 to 40 years", "minimum age 18", "aged 18+", "18+ years"
        age_patterns = [
            re.compile(r"aged?\s+(\d{1,2})\s*[-–to]+\s*(\d{1,2})", re.IGNORECASE),
            re.compile(r"(\d{1,2})\s*[-–to]+\s*(\d{1,2})\s*years?\s*(?:old|of\s+age)?", re.IGNORECASE),
            re.compile(r"(?:aged?|age)\s+(\d{1,2})\s*(?:\+|and\s+above|or\s+above)", re.IGNORECASE),
            re.compile(r"(\d{1,2})\s*(?:\+|years?\s*(?:and\s+above|or\s+above))", re.IGNORECASE),
            re.compile(r"minimum\s+age\s*[:\s]*(\d{1,2})", re.IGNORECASE),
            re.compile(r"(?:above|over|atleast|at\s+least)\s+(\d{1,2})\s*(?:years?)?", re.IGNORECASE),
            re.compile(r"(?:below|under|up\s*to|maximum)\s+(\d{1,2})\s*(?:years?)?", re.IGNORECASE),
        ]

        for pattern in age_patterns:
            match = pattern.search(text)
            if match:
                groups = match.groups()
                if len(groups) == 2 and groups[0] and groups[1]:
                    min_age, max_age = int(groups[0]), int(groups[1])
                    if min_age > max_age:
                        min_age, max_age = max_age, min_age
                    scheme.age_range = AgeRange(min_age=min_age, max_age=max_age)
                elif len(groups) >= 1 and groups[0]:
                    age = int(groups[0])
                    match_str = match.group().lower()
                    if any(kw in match_str for kw in ["minimum", "above", "over", "+", "least"]):
                        scheme.age_range = AgeRange(min_age=age)
                    else:
                        scheme.age_range = AgeRange(max_age=age)
                return

    def _normalize_income_limit(self, scheme: Scheme):
        """Extract income limit from eligibility text if not already set."""
        if scheme.income_limit:
            return

        text = (scheme.eligibility_summary or "") + " " + (scheme.description or "")
        if not text.strip():
            return

        # Patterns: "₹2.5 lakh", "Rs. 8,00,000", "income below 2.5 lakh"
        income_patterns = [
            re.compile(r"income\s*(?:below|under|less\s+than|≤|<=|upto|up\s*to)?\s*(?:₹|Rs\.?\s*|INR\s*)"
                        r"([\d,]+(?:\.\d+)?)\s*(lakh|crore|lakhs?|crores?)?", re.IGNORECASE),
            re.compile(r"(?:₹|Rs\.?\s*|INR\s*)([\d,]+(?:\.\d+)?)\s*(lakh|crore|lakhs?|crores?)?"
                        r"\s*(?:per\s*(?:annum|year))?", re.IGNORECASE),
        ]

        for pattern in income_patterns:
            match = pattern.search(text)
            if match:
                amount_str = match.group(1).replace(",", "")
                multiplier_str = (match.group(2) or "").lower()

                try:
                    amount = float(amount_str)
                except ValueError:
                    continue

                if "lakh" in multiplier_str:
                    amount = int(amount * 100000)
                elif "crore" in multiplier_str:
                    amount = int(amount * 10000000)
                else:
                    amount = int(amount)

                scheme.income_limit = IncomeLimit(
                    amount=amount,
                    currency="INR",
                    period="annual",
                    basis="family",
                    raw_text=match.group(0).strip(),
                )
                return

    def _normalize_benefit_type(self, scheme: Scheme):
        """Infer benefit type from text if not set."""
        if scheme.benefit_type and scheme.benefit_type != BenefitType.OTHER:
            return

        text = ((scheme.benefits or "") + " " + (scheme.description or "")).lower()

        type_keywords = {
            BenefitType.SCHOLARSHIP: ["scholarship", "stipend", "fellowship", "tuition"],
            BenefitType.LOAN: ["loan", "credit", "lending", "mudra"],
            BenefitType.SUBSIDY: ["subsidy", "subsidized", "subvention"],
            BenefitType.INSURANCE: ["insurance", "bima", "coverage", "premium"],
            BenefitType.TRAINING: ["training", "skill", "course", "certification"],
            BenefitType.JOB: ["employment", "job", "placement", "recruitment"],
            BenefitType.HOUSING: ["housing", "awas", "shelter", "house"],
            BenefitType.FINANCIAL: ["₹", "rs.", "financial", "assistance", "cash", "pension", "amount"],
        }

        for bt, keywords in type_keywords.items():
            if any(kw in text for kw in keywords):
                scheme.benefit_type = bt
                return

    def _normalize_application_mode(self, scheme: Scheme):
        """Detect application mode from text."""
        if scheme.application_mode != ApplicationMode.UNKNOWN:
            return

        text = ((scheme.application_url or "") + " " +
                " ".join(scheme.application_steps) + " " +
                (scheme.eligibility_summary or "")).lower()

        has_online = any(kw in text for kw in ["online", "portal", "website", ".gov.in", ".nic.in", "https://"])

        # Check offline: distinguish physical submission/offices from "visit the website/portal"
        offline_keywords = [
            "offline", "in person", "in-person", "panchayat", "bank branch",
            "district office", "taluk office", "csc centre", "csc center",
            "meeseva", "mee seva", "gram panchayat", "collectorate",
        ]
        has_offline = any(kw in text for kw in offline_keywords)
        if not has_offline and "visit" in text:
            # Physical visit to an office or location (not just "visit portal" or "visit website")
            if re.search(r"visit\s+(?:the\s+)?(?:nearest\s+|local\s+)?(?:office|branch|centre|center|panchayat|bdo|dept|kendra)", text):
                has_offline = True

        if has_online and has_offline:
            scheme.application_mode = ApplicationMode.BOTH
        elif has_online:
            scheme.application_mode = ApplicationMode.ONLINE
        elif has_offline:
            scheme.application_mode = ApplicationMode.OFFLINE

    def _normalize_category(self, scheme: Scheme):
        """Infer category from scheme text if not set."""
        if scheme.category:
            return

        text = ((scheme.name or "") + " " + (scheme.description or "") + " " +
                (scheme.eligibility_summary or "")).lower()

        cat_keywords = {
            Category.FARMER: ["farmer", "kisan", "agriculture", "crop", "land", "rythu"],
            Category.STUDENT: ["student", "scholarship", "education", "school", "college"],
            Category.JOB_SEEKER: ["employment", "skill", "job", "training", "worker"],
            Category.WOMEN: ["women", "woman", "girl", "maternity", "widow", "mahila"],
            Category.ENTREPRENEUR: ["business", "startup", "entrepreneur", "enterprise", "mudra"],
            Category.SENIOR_CITIZEN: ["senior", "pension", "old age", "elderly", "60+", "65+"],
            Category.MINORITY: ["minority", "tribal", "tribal"],
        }

        for cat, keywords in cat_keywords.items():
            if any(kw in text for kw in keywords):
                scheme.category = cat
                return

        scheme.category = Category.GENERAL

    def _normalize_documents(self, scheme: Scheme):
        """Clean and deduplicate required documents."""
        if not scheme.required_documents:
            return

        seen = set()
        cleaned = []
        for doc in scheme.required_documents:
            doc = doc.strip()
            # Remove numbering
            doc = re.sub(r"^\d+[\.\)]\s*", "", doc)
            doc_lower = doc.lower()
            if doc and doc_lower not in seen and len(doc) > 3:
                seen.add(doc_lower)
                cleaned.append(doc)

        scheme.required_documents = cleaned

    def _normalize_tags(self, scheme: Scheme):
        """Generate tags from scheme content."""
        if scheme.tags:
            return

        tags = set()
        text = ((scheme.name or "") + " " + (scheme.description or "")).lower()

        tag_keywords = [
            "farmer", "kisan", "agriculture", "student", "scholarship",
            "women", "pension", "loan", "subsidy", "insurance", "training",
            "skill", "housing", "health", "education", "employment",
            "startup", "entrepreneur", "SC", "ST", "OBC", "minority",
        ]

        for kw in tag_keywords:
            if kw.lower() in text:
                tags.add(kw.lower())

        if scheme.state:
            tags.add(scheme.state.lower())

        if scheme.category:
            tags.add(scheme.category.value.lower())

        scheme.tags = sorted(tags)

    def _extract_eligibility_rules(self, scheme: Scheme):
        """
        Extract structured eligibility rules from the eligibility summary.
        This is a best-effort extraction — complex rules need human review.
        """
        if scheme.eligibility_rules:
            return

        text = scheme.eligibility_summary or ""
        if not text:
            return

        rules: list[EligibilityRule] = []

        # Age rules (if age_range was extracted)
        if scheme.age_range:
            if scheme.age_range.min_age:
                rules.append(EligibilityRule(
                    field="age", operator="GTE",
                    value=str(scheme.age_range.min_age),
                    description=f"Must be {scheme.age_range.min_age} years or older",
                    source_evidence=text,
                ))
            if scheme.age_range.max_age:
                rules.append(EligibilityRule(
                    field="age", operator="LTE",
                    value=str(scheme.age_range.max_age),
                    description=f"Must be {scheme.age_range.max_age} years or younger",
                    source_evidence=text,
                ))

        # Income rules
        if scheme.income_limit and scheme.income_limit.amount:
            rules.append(EligibilityRule(
                field="annual_income", operator="LTE",
                value=str(scheme.income_limit.amount),
                description=f"Family income must be below ₹{scheme.income_limit.amount:,}",
                source_evidence=scheme.income_limit.raw_text or text,
            ))

        # Category rules
        text_lower = text.lower()
        if "scheduled caste" in text_lower or "sc " in text_lower or "sc/" in text_lower:
            if "sc/st" in text_lower:
                rules.append(EligibilityRule(
                    field="social_category", operator="IN",
                    value="SC,ST",
                    description="Must be SC or ST",
                    source_evidence=text,
                ))
            elif "sc/st/obc" in text_lower:
                rules.append(EligibilityRule(
                    field="social_category", operator="IN",
                    value="SC,ST,OBC",
                    description="Must be SC, ST, or OBC",
                    source_evidence=text,
                ))
            else:
                rules.append(EligibilityRule(
                    field="social_category", operator="EQ",
                    value="SC",
                    description="Must be Scheduled Caste",
                    source_evidence=text,
                ))

        # Farmer rule
        if any(kw in text_lower for kw in ["farmer", "kisan", "landholding", "cultivable"]):
            rules.append(EligibilityRule(
                field="is_farmer", operator="EQ",
                value="true",
                description="Must be a farmer",
                source_evidence=text,
            ))

        # Student rule
        if any(kw in text_lower for kw in ["student", "enrolled", "admitted", "pursuing"]):
            rules.append(EligibilityRule(
                field="is_student", operator="EQ",
                value="true",
                description="Must be a student",
                source_evidence=text,
            ))

        # Gender rule
        if any(kw in text_lower for kw in ["women only", "girl student", "must be a woman", "female"]):
            rules.append(EligibilityRule(
                field="gender", operator="EQ",
                value="FEMALE",
                description="Must be female",
                source_evidence=text,
            ))

        # State rule
        if scheme.state:
            rules.append(EligibilityRule(
                field="state", operator="EQ",
                value=scheme.state,
                description=f"Must be from {scheme.state}",
                source_evidence=text,
            ))

        scheme.eligibility_rules = rules

    def _normalize_exclusions(self, scheme: Scheme):
        """Extract exclusion conditions from eligibility text."""
        if scheme.exclusions:
            return

        text = scheme.eligibility_summary or ""
        exclusions = []

        # Common exclusion patterns
        excl_patterns = [
            re.compile(r"(?:exclud|not\s+eligibl|ineligibl|except|not\s+applicable\s+(?:to|for))[:\s]*(.+?)(?:\.|$)", re.IGNORECASE),
            re.compile(r"(?:should\s+not|must\s+not|cannot)\s+(?:be|have)\s+(.+?)(?:\.|$)", re.IGNORECASE),
        ]

        for pattern in excl_patterns:
            for match in pattern.finditer(text):
                excl_text = match.group(1).strip()
                if excl_text and len(excl_text) > 5:
                    exclusions.append(excl_text)

        scheme.exclusions = exclusions

"""
JanSetuAI — Duplicate Detection
=================================
Identifies duplicate and near-duplicate schemes using
name similarity, slug matching, and source URL comparison.
"""

from __future__ import annotations

import logging
import re
from difflib import SequenceMatcher
from typing import Optional

from data_pipeline.validation.schema import Scheme

logger = logging.getLogger(__name__)


class DuplicateDetector:
    """
    Detects duplicate schemes using multiple strategies:
    1. Exact slug match
    2. Exact source URL match
    3. Name similarity (fuzzy matching)
    4. Scheme ID collision
    """

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        self._existing: list[Scheme] = []
        self._slug_index: dict[str, int] = {}
        self._url_index: dict[str, int] = {}
        self._id_index: dict[str, int] = {}

    def load_existing(self, schemes: list[Scheme]):
        """Load existing schemes for duplicate checking."""
        self._existing = schemes
        self._slug_index.clear()
        self._url_index.clear()
        self._id_index.clear()

        for idx, s in enumerate(schemes):
            if s.slug:
                self._slug_index[s.slug.lower()] = idx
            if s.source_url:
                self._url_index[self._normalize_url(s.source_url)] = idx
            if s.scheme_id:
                self._id_index[s.scheme_id] = idx

    def find_duplicate(self, candidate: Scheme) -> Optional[DuplicateMatch]:
        """
        Check if candidate is a duplicate of any existing scheme.
        Returns DuplicateMatch if found, None otherwise.
        """
        # 1. Exact scheme ID match
        if candidate.scheme_id and candidate.scheme_id in self._id_index:
            idx = self._id_index[candidate.scheme_id]
            return DuplicateMatch(
                existing=self._existing[idx],
                candidate=candidate,
                match_type="scheme_id",
                confidence=1.0,
            )

        # 2. Exact slug match
        if candidate.slug:
            slug_key = candidate.slug.lower()
            if slug_key in self._slug_index:
                idx = self._slug_index[slug_key]
                return DuplicateMatch(
                    existing=self._existing[idx],
                    candidate=candidate,
                    match_type="slug",
                    confidence=1.0,
                )

        # 3. Exact URL match
        if candidate.source_url:
            url_key = self._normalize_url(candidate.source_url)
            if url_key in self._url_index:
                idx = self._url_index[url_key]
                return DuplicateMatch(
                    existing=self._existing[idx],
                    candidate=candidate,
                    match_type="source_url",
                    confidence=0.95,
                )

        # 4. Name similarity
        if candidate.name:
            best_match = self._find_name_match(candidate)
            if best_match:
                return best_match

        return None

    def deduplicate_batch(self, schemes: list[Scheme]) -> tuple[list[Scheme], list[DuplicateMatch]]:
        """
        Deduplicate a batch of schemes.
        Returns (unique_schemes, duplicate_matches).
        """
        unique: list[Scheme] = []
        duplicates: list[DuplicateMatch] = []

        # Build index from existing + already-accepted candidates
        working_set = list(self._existing)

        for candidate in schemes:
            # Check against existing + already accepted
            self.load_existing(working_set)
            match = self.find_duplicate(candidate)

            if match:
                duplicates.append(match)
                logger.info(
                    f"Duplicate found: '{candidate.name}' matches "
                    f"'{match.existing.name}' ({match.match_type}, {match.confidence:.2f})"
                )
            else:
                unique.append(candidate)
                working_set.append(candidate)

        return unique, duplicates

    def _find_name_match(self, candidate: Scheme) -> Optional[DuplicateMatch]:
        """Find the best name match using fuzzy string matching."""
        if not candidate.name:
            return None
        name_clean = self._clean_name(candidate.name)
        if not name_clean:
            return None

        best_score = 0.0
        best_idx = -1

        for idx, existing in enumerate(self._existing):
            if not existing.name:
                continue
            existing_clean = self._clean_name(existing.name)
            if not existing_clean:
                continue

            # If cleaned strings are very short (< 4 chars), require exact match
            if len(name_clean) < 4 or len(existing_clean) < 4:
                score = 1.0 if name_clean == existing_clean else 0.0
            else:
                score = SequenceMatcher(None, name_clean, existing_clean).ratio()

            if score > best_score:
                best_score = score
                best_idx = idx

        if best_score >= self.similarity_threshold and best_idx >= 0:
            return DuplicateMatch(
                existing=self._existing[best_idx],
                candidate=candidate,
                match_type="name_similarity",
                confidence=best_score,
            )

        return None

    def _clean_name(self, name: str) -> str:
        """Clean and normalize a scheme name for comparison."""
        name_lower = name.lower().strip()
        cleaned = name_lower
        # Remove common prefixes and generic scheme words
        for term in [
            "pradhan mantri", "pm-", "pm ", "national ", "central ",
            "scheme", "yojana", "yojna", "karyakramam", "mission",
        ]:
            cleaned = cleaned.replace(term, "")
        # Remove special chars
        cleaned = re.sub(r"[^a-z0-9\s]", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        if not cleaned:
            # Fallback to stripping just special chars if all words were removed
            return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", "", name_lower)).strip()

        return cleaned

    def _normalize_url(self, url: str) -> str:
        """Normalize a URL for comparison."""
        url = url.lower().strip().rstrip("/")
        url = re.sub(r"^https?://", "", url)
        url = re.sub(r"^www\.", "", url)
        return url


class DuplicateMatch:
    """Represents a detected duplicate."""

    def __init__(
        self,
        existing: Scheme,
        candidate: Scheme,
        match_type: str,
        confidence: float,
    ):
        self.existing = existing
        self.candidate = candidate
        self.match_type = match_type
        self.confidence = confidence

    def __repr__(self):
        return (
            f"DuplicateMatch('{self.candidate.name}' ≈ '{self.existing.name}', "
            f"type={self.match_type}, conf={self.confidence:.2f})"
        )

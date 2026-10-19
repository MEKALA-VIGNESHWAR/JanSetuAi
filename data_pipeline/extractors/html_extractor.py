"""
JanSetuAI — HTML Extractor
===========================
Extracts scheme-related fields from HTML pages using BeautifulSoup.
Works with government portal layouts that vary widely.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


class HTMLExtractor:
    """
    Extracts scheme fields from HTML content.
    Uses heuristic matching on headings and section labels
    common in government websites.
    """

    # Section heading patterns
    SECTION_PATTERNS = {
        "name": re.compile(r"scheme\s*name|title|heading", re.IGNORECASE),
        "description": re.compile(r"about|description|overview|details|introduction|objective", re.IGNORECASE),
        "benefits": re.compile(r"benefits?|entitlement|amount|assistance|incentive", re.IGNORECASE),
        "eligibility": re.compile(r"eligib|criteria|who\s*can|qualification|condition", re.IGNORECASE),
        "documents": re.compile(r"document|requirement|paper|certificate|proof", re.IGNORECASE),
        "application": re.compile(r"how\s*to\s*apply|application|process|procedure|apply\s*online", re.IGNORECASE),
        "department": re.compile(r"ministry|department|authority|implement", re.IGNORECASE),
    }

    def extract_scheme_fields(self, html: str, base_url: str = "") -> dict[str, Any]:
        """
        Extract scheme-related fields from an HTML page.
        Returns a dict with extracted fields.
        """
        soup = BeautifulSoup(html, "lxml")
        result: dict[str, Any] = {}

        # Remove script and style
        for tag in soup.find_all(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Extract title
        result["name"] = self._extract_title(soup)

        # Extract meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            result["short_description"] = str(meta_desc["content"]).strip()

        # Try section-based extraction
        sections = self._find_sections(soup)
        for field, content in sections.items():
            result[field] = content

        # Extract links that look like application URLs
        app_url = self._find_application_url(soup, base_url)
        if app_url:
            result["application_url"] = app_url

        # Extract document lists
        if "documents" not in result:
            docs = self._extract_document_list(soup)
            if docs:
                result["documents"] = docs

        return result

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the page/scheme title."""
        # Try h1 first
        h1 = soup.find("h1")
        if h1:
            text = h1.get_text(strip=True)
            if len(text) > 5:
                return text

        # Try <title> tag
        title = soup.find("title")
        if title:
            text = title.get_text(strip=True)
            # Clean common suffixes
            for suffix in [" - myScheme", " | Government of India", " | Telangana"]:
                text = text.replace(suffix, "")
            return text.strip()

        return ""

    def _find_sections(self, soup: BeautifulSoup) -> dict[str, str]:
        """
        Find and extract content under section headings.
        Government pages often use h2/h3/h4 or div labels.
        """
        sections: dict[str, str] = {}
        headings = soup.find_all(["h2", "h3", "h4", "h5", "strong", "b"])

        for heading in headings:
            heading_text = heading.get_text(strip=True)
            if len(heading_text) < 3 or len(heading_text) > 100:
                continue

            for field, pattern in self.SECTION_PATTERNS.items():
                if pattern.search(heading_text) and field not in sections:
                    content = self._get_section_content(heading)
                    if content and len(content) > 10:
                        sections[field] = content
                    break

        return sections

    def _get_section_content(self, heading: Tag) -> str:
        """
        Get the text content following a heading tag,
        up to the next heading of the same or higher level.
        """
        parts: list[str] = []
        tag_name = heading.name if heading.name in ("h2", "h3", "h4", "h5") else "h4"
        stop_tags = {"h1", "h2", "h3"} if tag_name in ("h3", "h4", "h5") else {"h1", "h2"}

        sibling = heading.find_next_sibling()
        max_parts = 20  # safety limit
        while sibling and max_parts > 0:
            if sibling.name in stop_tags:
                break
            text = sibling.get_text(strip=True)
            if text:
                parts.append(text)
            sibling = sibling.find_next_sibling()
            max_parts -= 1

        return "\n".join(parts)

    def _find_application_url(self, soup: BeautifulSoup, base_url: str) -> str | None:
        """Find links that look like application/registration URLs."""
        apply_patterns = re.compile(
            r"apply|register|enroll|portal|login|sign.up|application.form",
            re.IGNORECASE,
        )

        for a_tag in soup.find_all("a", href=True):
            link_text = a_tag.get_text(strip=True).lower()
            href = str(a_tag["href"])

            if apply_patterns.search(link_text) or apply_patterns.search(href):
                if href.startswith("http"):
                    return href
                elif href.startswith("/"):
                    return urljoin(base_url, href)

        return None

    def _extract_document_list(self, soup: BeautifulSoup) -> list[str]:
        """Extract document requirements from list elements."""
        docs: list[str] = []
        doc_pattern = re.compile(
            r"aadhaar|pan\s*card|income|caste|certificate|passbook|marksheet|"
            r"passport|domicile|proof|bank|photograph|affidavit",
            re.IGNORECASE,
        )

        for li in soup.find_all("li"):
            text = li.get_text(strip=True)
            if doc_pattern.search(text) and 10 < len(text) < 200:
                docs.append(text)

        return docs[:20]  # cap at 20

    def extract_text_content(self, html: str) -> str:
        """Extract clean text from HTML, useful for PDF-like text processing."""
        soup = BeautifulSoup(html, "lxml")
        for tag in soup.find_all(["script", "style"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)

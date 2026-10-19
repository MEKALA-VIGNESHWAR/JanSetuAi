"""
JanSetuAI — PDF Extractor
===========================
Extracts text from PDF documents (official scheme guidelines,
notifications, circulars). Uses PyMuPDF for text extraction.
Flags low-confidence extraction for human review.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

try:
    import fitz  # PyMuPDF
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False
    logger.warning("PyMuPDF not installed. PDF extraction will be unavailable.")


class PDFExtractor:
    """
    Extracts text and structured fields from PDF documents.
    Supports text-based PDFs. Flags scanned/image PDFs
    as needing OCR (future enhancement).
    """

    # Minimum text density to consider a page as text-based (vs scanned)
    MIN_TEXT_DENSITY = 50  # characters per page

    def __init__(self):
        if not HAS_PYMUPDF:
            raise ImportError(
                "PyMuPDF is required for PDF extraction. "
                "Install it with: pip install PyMuPDF"
            )

    def extract_text(self, pdf_path: str) -> dict[str, Any]:
        """
        Extract all text from a PDF file.
        
        Returns:
            dict with keys:
                - text: full extracted text
                - pages: number of pages
                - is_scanned: True if the PDF appears to be scanned/image-based
                - confidence: extraction confidence (high, medium, low)
                - metadata: PDF metadata dict
        """
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        doc = fitz.open(str(path))
        all_text: list[str] = []
        page_texts: list[str] = []
        low_text_pages = 0

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text")
            page_texts.append(text)
            all_text.append(text)

            if len(text.strip()) < self.MIN_TEXT_DENSITY:
                low_text_pages += 1

        full_text = "\n\n".join(all_text)
        total_pages = len(doc)
        is_scanned = low_text_pages > total_pages * 0.5  # majority pages low-text

        # Determine confidence
        if is_scanned:
            confidence = "low"
        elif low_text_pages > 0:
            confidence = "medium"
        else:
            confidence = "high"

        metadata = doc.metadata or {}
        doc.close()

        return {
            "text": full_text,
            "pages": total_pages,
            "is_scanned": is_scanned,
            "confidence": confidence,
            "metadata": metadata,
            "page_texts": page_texts,
        }

    def extract_scheme_fields(self, pdf_path: str) -> dict[str, Any]:
        """
        Extract and attempt to identify scheme-related fields
        from a PDF document.
        """
        result = self.extract_text(pdf_path)
        text = result["text"]
        fields: dict[str, Any] = {
            "source_file": pdf_path,
            "extraction_confidence": result["confidence"],
            "is_scanned": result["is_scanned"],
            "pages": result["pages"],
        }

        if result["is_scanned"]:
            fields["needs_ocr"] = True
            fields["review_flag"] = "Scanned PDF — needs OCR and human review"
            return fields

        # Extract common scheme patterns from text
        fields["name"] = self._extract_scheme_name(text)
        fields["eligibility"] = self._extract_section(text, r"eligib|criteria|qualification")
        fields["benefits"] = self._extract_section(text, r"benefits?|entitlement|assistance")
        fields["documents"] = self._extract_section(text, r"documents?|requirement|certificate")
        fields["application"] = self._extract_section(text, r"application|procedure|how\s*to\s*apply")

        # Extract monetary amounts
        fields["amounts"] = self._extract_amounts(text)

        # Extract dates
        fields["dates"] = self._extract_dates(text)

        return fields

    def _extract_scheme_name(self, text: str) -> str:
        """Try to extract the scheme name from the first lines."""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        # First non-trivial line is often the title
        for line in lines[:10]:
            if 10 < len(line) < 200 and not line.startswith("Page"):
                return line
        return ""

    def _extract_section(self, text: str, pattern: str) -> str:
        """
        Find a section matching the pattern and extract its content.
        """
        section_re = re.compile(
            rf"^[#\s]*(?:[\d.]*\s*)?({pattern})[:\s\-—]*$",
            re.IGNORECASE | re.MULTILINE,
        )
        match = section_re.search(text)
        if not match:
            return ""

        start = match.end()
        # Read until next section heading or limit
        next_section = re.search(
            r"^\s*(?:[\d.]+\s+)?[A-Z][a-z]+(?:\s+[A-Za-z]+){0,4}\s*[:]\s*$",
            text[start:],
            re.MULTILINE,
        )
        end = start + (next_section.start() if next_section else 2000)
        return text[start:end].strip()[:2000]

    def _extract_amounts(self, text: str) -> list[str]:
        """Extract monetary amounts (₹, Rs., INR patterns)."""
        amount_re = re.compile(
            r"(?:₹|Rs\.?\s*|INR\s*)"
            r"[\d,]+(?:\.\d{1,2})?"
            r"(?:\s*(?:lakh|crore|thousand|per\s+\w+|/\w+))?",
            re.IGNORECASE,
        )
        matches = amount_re.findall(text)
        return list(set(matches))[:10]

    def _extract_dates(self, text: str) -> list[str]:
        """Extract dates from the document."""
        date_re = re.compile(
            r"\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}"
            r"|(?:January|February|March|April|May|June|July|August|"
            r"September|October|November|December)\s+\d{1,2},?\s*\d{4}",
            re.IGNORECASE,
        )
        matches = date_re.findall(text)
        return list(set(matches))[:10]

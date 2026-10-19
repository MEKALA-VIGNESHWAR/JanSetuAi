"""
JanSetuAI — Base Source Collector
==================================
Abstract base class for all source collectors. Each source
(myScheme, Telangana portal, etc.) implements its own adapter.
"""

from __future__ import annotations

import json
import logging
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from data_pipeline.validation.schema import RawSourceSnapshot, Scheme

logger = logging.getLogger(__name__)


class BaseCollector(ABC):
    """
    Base class providing HTTP fetching with retries, rate limiting,
    and raw snapshot storage. Subclasses implement discover() and
    extract_scheme().
    """

    def __init__(
        self,
        source_name: str,
        base_url: str,
        raw_data_dir: str = "data/raw",
        request_delay: float = 1.5,
        timeout: float = 30.0,
    ):
        self.source_name = source_name
        self.base_url = base_url.rstrip("/")
        self.raw_data_dir = Path(raw_data_dir) / source_name
        self.request_delay = request_delay
        self.timeout = timeout
        self._last_request_time = 0.0

        # Create directories
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

        # HTTP client with sensible defaults
        self.client = httpx.Client(
            timeout=httpx.Timeout(timeout),
            follow_redirects=True,
            headers={
                "User-Agent": "JanSetuAI-DataPipeline/1.0 (educational project; +https://github.com/jansetuai)",
                "Accept": "text/html,application/json,application/xhtml+xml",
                "Accept-Language": "en-IN,en;q=0.9,hi;q=0.8",
            },
        )

    def _rate_limit(self):
        """Enforce minimum delay between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        self._last_request_time = time.time()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
    )
    def fetch_url(self, url: str) -> httpx.Response:
        """Fetch a URL with rate limiting and retries."""
        self._rate_limit()
        logger.info(f"[{self.source_name}] Fetching: {url}")
        response = self.client.get(url)
        response.raise_for_status()
        return response

    def save_raw_snapshot(
        self,
        url: str,
        content: str,
        content_type: str = "html",
        http_status: int = 200,
        extra_name: str = "",
    ) -> RawSourceSnapshot:
        """
        Save raw content to disk and return a snapshot record.
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_name = url.split("/")[-1][:60] or "index"
        safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in safe_name)
        if extra_name:
            safe_name = f"{extra_name}_{safe_name}"

        ext = {"html": ".html", "json": ".json", "pdf": ".pdf", "text": ".txt"}.get(content_type, ".txt")
        filename = f"{timestamp}_{safe_name}{ext}"
        filepath = self.raw_data_dir / filename

        filepath.write_text(content, encoding="utf-8")
        logger.info(f"[{self.source_name}] Saved raw snapshot: {filepath}")

        return RawSourceSnapshot(
            source_name=self.source_name,
            url=url,
            retrieved_at=datetime.utcnow(),
            content_type=content_type,
            raw_file_path=str(filepath),
            http_status=http_status,
        )

    def save_raw_binary(
        self,
        url: str,
        content: bytes,
        content_type: str = "pdf",
        http_status: int = 200,
    ) -> RawSourceSnapshot:
        """Save binary content (PDF etc.) to disk."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_name = url.split("/")[-1][:60] or "document"
        safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in safe_name)
        ext = {"pdf": ".pdf", "image": ".png"}.get(content_type, ".bin")
        filename = f"{timestamp}_{safe_name}{ext}"
        filepath = self.raw_data_dir / filename

        filepath.write_bytes(content)
        logger.info(f"[{self.source_name}] Saved raw binary: {filepath}")

        return RawSourceSnapshot(
            source_name=self.source_name,
            url=url,
            retrieved_at=datetime.utcnow(),
            content_type=content_type,
            raw_file_path=str(filepath),
            http_status=http_status,
        )

    @abstractmethod
    def discover(self) -> list[dict[str, Any]]:
        """
        Discover scheme URLs/entries from this source.
        Returns list of dicts with at minimum {'url': ..., 'name': ...}.
        """
        ...

    @abstractmethod
    def extract_scheme(self, entry: dict[str, Any]) -> Scheme | None:
        """
        Given a discovered entry, fetch details and return a Scheme
        object, or None if extraction fails.
        """
        ...

    def collect_all(self) -> list[Scheme]:
        """Run full collection: discover → extract for each entry."""
        schemes: list[Scheme] = []
        entries = self.discover()
        logger.info(f"[{self.source_name}] Discovered {len(entries)} entries")

        for entry in entries:
            try:
                scheme = self.extract_scheme(entry)
                if scheme:
                    schemes.append(scheme)
                    logger.info(f"[{self.source_name}] Extracted: {scheme.name}")
            except Exception as e:
                logger.error(f"[{self.source_name}] Failed to extract {entry}: {e}")

        logger.info(f"[{self.source_name}] Collected {len(schemes)} schemes total")
        return schemes

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

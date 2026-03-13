"""
crawler.py — Passive web crawler for route and endpoint inventory.

Crawls same-origin links breadth-first. Passive only — no form submissions,
no authentication, no payload injection. Respects robots.txt by default.

Used by the full audit workflow to build an attack surface map.
"""

from __future__ import annotations

import logging
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

from src.parsers.html_parser import PageInventory, parse_page
from src.utils.evidence_writer import write_evidence
from src.utils.http_client import HttpClient

logger = logging.getLogger(__name__)

DOMAIN = "Information Gathering"
EVIDENCE_TYPE = "Tool Output"


@dataclass
class CrawlResult:
    """Aggregate output of a crawl run."""
    seed_url: str
    pages: List[PageInventory] = field(default_factory=list)
    errors: Dict[str, str] = field(default_factory=dict)   # url → error message
    skipped: List[str] = field(default_factory=list)        # out-of-scope URLs noted
    forms_found: int = 0
    scripts_found: int = 0
    iframes_found: int = 0


class Crawler:
    """
    Passive same-origin web crawler.

    Default limits are deliberately conservative to avoid accidental
    load on production environments (see safety-authorization-rules.md Rule 6).
    """

    def __init__(
        self,
        http_client: HttpClient,
        collector: str,
        max_pages: int = 50,
        delay_seconds: float = 0.5,
        respect_robots: bool = True,
    ) -> None:
        self._client = http_client
        self._collector = collector
        self._max_pages = max_pages
        self._delay = delay_seconds
        self._respect_robots = respect_robots

    def crawl(self, seed_url: str) -> CrawlResult:
        """
        Crawl from seed_url, collecting same-origin page inventories.
        Returns a CrawlResult with all discovered pages and surface data.
        """
        result = CrawlResult(seed_url=seed_url)
        seed_parsed = urlparse(seed_url)
        allowed_netloc = seed_parsed.netloc

        disallowed = self._fetch_robots_disallowed(seed_url) if self._respect_robots else set()

        visited: Set[str] = set()
        queue: deque = deque([seed_url])

        while queue and len(result.pages) < self._max_pages:
            url = queue.popleft()
            if url in visited:
                continue

            # Check out-of-scope (different host)
            parsed = urlparse(url)
            if parsed.netloc != allowed_netloc:
                result.skipped.append(url)
                continue

            # Check robots.txt
            path = parsed.path or "/"
            if any(path.startswith(d) for d in disallowed):
                logger.info("Skipping robots.txt-disallowed path: %s", path)
                result.skipped.append(url)
                visited.add(url)
                continue

            visited.add(url)

            response = self._client.get(url)
            if response is None:
                result.errors[url] = "HTTP request failed"
                continue

            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                continue

            inventory = parse_page(
                url=response.url,
                html=response.text,
                status_code=response.status_code,
                response_headers=dict(response.headers),
            )
            result.pages.append(inventory)
            result.forms_found += len(inventory.forms)
            result.scripts_found += len(inventory.scripts)
            result.iframes_found += len(inventory.iframes)

            for link in inventory.links:
                if link not in visited:
                    queue.append(link)

            if self._delay > 0:
                time.sleep(self._delay)

        # Write evidence summary
        self._write_crawl_evidence(result, seed_url)

        logger.info(
            "Crawl complete for %s — %d pages, %d forms, %d scripts, %d errors",
            seed_url,
            len(result.pages),
            result.forms_found,
            result.scripts_found,
            len(result.errors),
        )
        return result

    def _fetch_robots_disallowed(self, seed_url: str) -> Set[str]:
        """Fetch robots.txt and return the set of disallowed paths for *."""
        disallowed: Set[str] = set()
        parsed = urlparse(seed_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        response = self._client.get(robots_url)
        if response is None or response.status_code != 200:
            return disallowed
        current_agent = False
        for line in response.text.splitlines():
            line = line.strip()
            if line.lower().startswith("user-agent:"):
                agent = line.split(":", 1)[1].strip()
                current_agent = agent == "*"
            elif current_agent and line.lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if path:
                    disallowed.add(path)
        return disallowed

    def _write_crawl_evidence(self, result: CrawlResult, seed_url: str) -> Optional[str]:
        pages_summary = "\n".join(
            f"  [{p.status_code}] {p.url} — {len(p.forms)} form(s), {len(p.scripts)} script(s), title: {p.title[:60]}"
            for p in result.pages
        ) or "  (no pages crawled)"

        errors_summary = "\n".join(
            f"  {url}: {err}" for url, err in result.errors.items()
        ) or "  (none)"

        content = (
            f"Seed URL: {seed_url}\n"
            f"Pages discovered: {len(result.pages)}\n"
            f"Forms found: {result.forms_found}\n"
            f"External scripts: {result.scripts_found}\n"
            f"iframes: {result.iframes_found}\n"
            f"Pages skipped (out-of-scope or robots.txt): {len(result.skipped)}\n\n"
            f"Pages Crawled:\n{pages_summary}\n\n"
            f"Errors:\n{errors_summary}"
        )

        try:
            label, _ = write_evidence(
                description=f"Passive crawl surface inventory — {urlparse(seed_url).netloc}",
                domain=DOMAIN,
                evidence_type=EVIDENCE_TYPE,
                content=content,
                collector=self._collector,
                target=seed_url,
                observations=(
                    f"Passive crawl of {seed_url} discovered {len(result.pages)} pages, "
                    f"{result.forms_found} forms, and {result.scripts_found} external scripts. "
                    f"No form submissions or authenticated requests were made."
                ),
            )
            return label
        except Exception as exc:
            logger.error("Could not write crawl evidence: %s", exc)
            return None

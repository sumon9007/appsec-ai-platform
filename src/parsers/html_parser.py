"""
html_parser.py — Extract links, forms, inputs, and scripts from HTML responses.

Used by the crawler and input validation audit tool.
Requires beautifulsoup4 (in requirements.txt).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)


@dataclass
class HtmlForm:
    action: str
    method: str          # GET / POST
    inputs: List[dict]   # list of {name, type, required}
    enctype: str = "application/x-www-form-urlencoded"


@dataclass
class PageInventory:
    url: str
    status_code: int
    title: str = ""
    links: List[str] = field(default_factory=list)
    forms: List[HtmlForm] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)   # src of external scripts
    inline_scripts: int = 0                             # count of inline <script> blocks
    iframes: List[str] = field(default_factory=list)
    comments: List[str] = field(default_factory=list)
    meta_generator: str = ""                            # <meta name="generator">
    server_header: str = ""


def parse_page(url: str, html: str, status_code: int, response_headers: dict) -> PageInventory:
    """
    Parse an HTML page and return a structured PageInventory.
    Falls back to regex-based extraction if BeautifulSoup is unavailable.
    """
    try:
        from bs4 import BeautifulSoup
        return _parse_with_bs4(url, html, status_code, response_headers, BeautifulSoup)
    except ImportError:
        logger.warning("beautifulsoup4 not installed — using basic regex parser for HTML.")
        return _parse_with_regex(url, html, status_code, response_headers)


def _parse_with_bs4(url, html, status_code, headers, BeautifulSoup) -> PageInventory:
    soup = BeautifulSoup(html, "html.parser")
    base_url = url

    inventory = PageInventory(url=url, status_code=status_code)
    inventory.server_header = headers.get("server", "")

    # Title
    title_tag = soup.find("title")
    inventory.title = title_tag.get_text(strip=True) if title_tag else ""

    # Generator meta
    generator = soup.find("meta", attrs={"name": re.compile(r"generator", re.IGNORECASE)})
    if generator:
        inventory.meta_generator = generator.get("content", "")

    # Links
    seen_links = set()
    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue
        absolute = urljoin(base_url, href)
        parsed = urlparse(absolute)
        # Keep only same-host links
        if parsed.netloc == urlparse(base_url).netloc and absolute not in seen_links:
            seen_links.add(absolute)
            inventory.links.append(absolute)

    # Forms
    for form in soup.find_all("form"):
        action = urljoin(base_url, form.get("action", ""))
        method = form.get("method", "GET").upper()
        enctype = form.get("enctype", "application/x-www-form-urlencoded")
        inputs = []
        for inp in form.find_all(["input", "textarea", "select"]):
            inputs.append({
                "name": inp.get("name", ""),
                "type": inp.get("type", "text"),
                "required": inp.has_attr("required"),
            })
        inventory.forms.append(HtmlForm(action=action, method=method, inputs=inputs, enctype=enctype))

    # External scripts
    for script in soup.find_all("script"):
        src = script.get("src", "")
        if src:
            inventory.scripts.append(urljoin(base_url, src))
        elif script.string and script.string.strip():
            inventory.inline_scripts += 1

    # iframes
    for iframe in soup.find_all("iframe", src=True):
        inventory.iframes.append(urljoin(base_url, iframe["src"]))

    # HTML comments (may reveal sensitive info)
    import re
    comments = re.findall(r"<!--(.*?)-->", html, re.DOTALL)
    inventory.comments = [c.strip()[:200] for c in comments if c.strip() and len(c.strip()) > 3]

    return inventory


def _parse_with_regex(url, html, status_code, headers) -> PageInventory:
    import re
    inventory = PageInventory(url=url, status_code=status_code)
    inventory.server_header = headers.get("server", "")

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    inventory.title = title_match.group(1).strip() if title_match else ""

    for href in re.findall(r'href=["\']([^"\']+)["\']', html, re.IGNORECASE):
        if not href.startswith(("#", "javascript:", "mailto:")):
            inventory.links.append(urljoin(url, href))

    inventory.scripts = [
        urljoin(url, src)
        for src in re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)
    ]
    inventory.inline_scripts = len(re.findall(r"<script(?![^>]+src=)[^>]*>", html, re.IGNORECASE))
    inventory.comments = re.findall(r"<!--(.*?)-->", html, re.DOTALL)[:10]
    return inventory


# need re in module scope for _parse_with_bs4
import re  # noqa: E402

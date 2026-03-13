"""
manifest.py — Dependency manifest parsers for multiple ecosystems.

Parses packages and versions from:
- requirements.txt / Pipfile (PyPI)
- package.json / package-lock.json (npm)
- pyproject.toml (PyPI)
- go.mod (Go)
- Gemfile.lock (RubyGems)
- composer.lock (Packagist)
- pom.xml (Maven — basic)

Returns a list of (package_name, version, ecosystem) tuples for OSV querying.
"""

from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path
from typing import List, Tuple

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore

logger = logging.getLogger(__name__)

Package = Tuple[str, str, str]   # (name, version, ecosystem)


def parse_manifest(manifest_path: Path) -> List[Package]:
    """
    Auto-detect manifest format and return a list of (name, version, ecosystem) tuples.
    Logs any lines it could not parse and continues.
    """
    path = Path(manifest_path)
    if not path.exists():
        logger.error("Manifest file not found: %s", path)
        return []

    name = path.name.lower()
    content = path.read_text(encoding="utf-8", errors="replace")

    if name in ("requirements.txt", "requirements-dev.txt", "requirements-test.txt"):
        return _parse_requirements_txt(content, path)
    if name == "pipfile":
        return _parse_pipfile(content, path)
    if name == "pyproject.toml":
        return _parse_pyproject_toml(content, path)
    if name == "package.json":
        return _parse_package_json(content, path)
    if name == "package-lock.json":
        return _parse_package_lock_json(content, path)
    if name == "go.mod":
        return _parse_go_mod(content, path)
    if name == "gemfile.lock":
        return _parse_gemfile_lock(content, path)
    if name == "composer.lock":
        return _parse_composer_lock(content, path)
    if name == "pom.xml":
        return _parse_pom_xml(content, path)

    logger.warning(
        "Unknown manifest format: %s. Supported: requirements.txt, package.json, "
        "pyproject.toml, go.mod, Gemfile.lock, composer.lock, pom.xml",
        path.name,
    )
    return []


def _parse_requirements_txt(content: str, path: Path) -> List[Package]:
    from packaging.requirements import Requirement, InvalidRequirement

    packages = []
    for i, line in enumerate(content.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        try:
            req = Requirement(line)
            version = next(iter(req.specifier), None)
            version_str = str(version).lstrip("=<>!~") if version else ""
            packages.append((req.name, version_str, "PyPI"))
        except (InvalidRequirement, Exception) as exc:
            logger.warning("%s line %d — could not parse: %r (%s)", path.name, i, line, exc)
    return packages


def _parse_pipfile(content: str, path: Path) -> List[Package]:
    if tomllib is None:
        logger.warning("tomllib/tomli not available — cannot parse Pipfile. Install tomli.")
        return []
    try:
        data = tomllib.loads(content)
        packages = []
        for section in ("packages", "dev-packages"):
            for name, spec in data.get(section, {}).items():
                version = spec if isinstance(spec, str) else ""
                version = version.strip("=<>!~*")
                packages.append((name, version, "PyPI"))
        return packages
    except Exception as exc:
        logger.warning("Could not parse Pipfile %s: %s", path, exc)
        return []


def _parse_pyproject_toml(content: str, path: Path) -> List[Package]:
    if tomllib is None:
        logger.warning("tomllib/tomli not available — cannot parse pyproject.toml.")
        return []
    try:
        data = tomllib.loads(content)
        deps = data.get("project", {}).get("dependencies", [])
        packages = []
        from packaging.requirements import Requirement, InvalidRequirement
        for dep in deps:
            try:
                req = Requirement(dep)
                version = next(iter(req.specifier), None)
                version_str = str(version).lstrip("=<>!~") if version else ""
                packages.append((req.name, version_str, "PyPI"))
            except (InvalidRequirement, Exception):
                logger.warning("Could not parse pyproject.toml dep: %r", dep)
        return packages
    except Exception as exc:
        logger.warning("Could not parse pyproject.toml %s: %s", path, exc)
        return []


def _parse_package_json(content: str, path: Path) -> List[Package]:
    try:
        data = json.loads(content)
        packages = []
        for section in ("dependencies", "devDependencies", "peerDependencies"):
            for name, version_spec in data.get(section, {}).items():
                version = re.sub(r"[^0-9.]", "", version_spec.split(" ")[0]) if isinstance(version_spec, str) else ""
                packages.append((name, version, "npm"))
        return packages
    except (json.JSONDecodeError, Exception) as exc:
        logger.warning("Could not parse package.json %s: %s", path, exc)
        return []


def _parse_package_lock_json(content: str, path: Path) -> List[Package]:
    try:
        data = json.loads(content)
        packages = []
        # v2/v3 lockfile uses "packages" key
        lock_packages = data.get("packages", {})
        for pkg_path, pkg_data in lock_packages.items():
            if not pkg_path or pkg_path == "":
                continue
            name = pkg_path.lstrip("node_modules/").split("/node_modules/")[-1]
            version = pkg_data.get("version", "")
            packages.append((name, version, "npm"))
        return packages
    except (json.JSONDecodeError, Exception) as exc:
        logger.warning("Could not parse package-lock.json %s: %s", path, exc)
        return []


def _parse_go_mod(content: str, path: Path) -> List[Package]:
    packages = []
    in_require = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("require ("):
            in_require = True
            continue
        if in_require and stripped == ")":
            in_require = False
            continue
        if stripped.startswith("require ") and not stripped.endswith("("):
            parts = stripped.split()
            if len(parts) >= 3:
                packages.append((parts[1], parts[2].lstrip("v"), "Go"))
            continue
        if in_require and stripped and not stripped.startswith("//"):
            parts = stripped.split()
            if len(parts) >= 2:
                packages.append((parts[0], parts[1].lstrip("v"), "Go"))
    return packages


def _parse_gemfile_lock(content: str, path: Path) -> List[Package]:
    packages = []
    in_gems = False
    for line in content.splitlines():
        if line.strip() == "GEM":
            in_gems = True
            continue
        if in_gems and line.strip() == "":
            in_gems = False
            continue
        if in_gems:
            match = re.match(r"\s{4}(\S+)\s+\(([^)]+)\)", line)
            if match:
                packages.append((match.group(1), match.group(2), "RubyGems"))
    return packages


def _parse_composer_lock(content: str, path: Path) -> List[Package]:
    try:
        data = json.loads(content)
        packages = []
        for pkg in data.get("packages", []) + data.get("packages-dev", []):
            name = pkg.get("name", "")
            version = pkg.get("version", "").lstrip("v")
            if name:
                packages.append((name, version, "Packagist"))
        return packages
    except (json.JSONDecodeError, Exception) as exc:
        logger.warning("Could not parse composer.lock %s: %s", path, exc)
        return []


def _parse_pom_xml(content: str, path: Path) -> List[Package]:
    packages = []
    # Simple regex-based extraction — good enough for majority of pom.xml files
    dep_pattern = re.compile(
        r"<dependency>.*?<groupId>([^<]+)</groupId>.*?<artifactId>([^<]+)</artifactId>"
        r"(?:.*?<version>([^<]+)</version>)?",
        re.DOTALL,
    )
    for match in dep_pattern.finditer(content):
        group = match.group(1).strip()
        artifact = match.group(2).strip()
        version = (match.group(3) or "").strip()
        # Skip property references like ${spring.version}
        if version.startswith("${"):
            version = ""
        packages.append((f"{group}:{artifact}", version, "Maven"))
    return packages

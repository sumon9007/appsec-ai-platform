"""
openapi_parser.py — Parse OpenAPI 2.x / 3.x specs and Postman collections.

Extracts endpoint inventory for API audit workflows.
Supports JSON and YAML formats.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ApiEndpoint:
    """A single API endpoint extracted from a spec."""
    method: str                          # GET, POST, PUT, etc.
    path: str                            # /api/users/{id}
    summary: str = ""
    parameters: List[Dict] = field(default_factory=list)
    requires_auth: bool = False
    request_body_schema: Optional[Dict] = None
    response_schemas: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    operation_id: str = ""


@dataclass
class ApiSpec:
    """Parsed API specification."""
    title: str
    version: str
    base_url: str
    endpoints: List[ApiEndpoint] = field(default_factory=list)
    security_schemes: List[str] = field(default_factory=list)
    spec_format: str = ""   # openapi3, swagger2, postman


def _load_spec_file(path: Path) -> Optional[Dict]:
    content = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix in (".yaml", ".yml"):
        try:
            import yaml
            return yaml.safe_load(content)
        except ImportError:
            logger.error("pyyaml is required to parse YAML specs. Install it: pip install pyyaml")
            return None
        except Exception as exc:
            logger.error("Could not parse YAML spec %s: %s", path, exc)
            return None
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        logger.error("Could not parse JSON spec %s: %s", path, exc)
        return None


def parse_spec(spec_path: Path) -> Optional[ApiSpec]:
    """
    Auto-detect and parse an OpenAPI or Postman spec file.
    Returns None if the file cannot be parsed.
    """
    path = Path(spec_path)
    if not path.exists():
        logger.error("Spec file not found: %s", path)
        return None

    data = _load_spec_file(path)
    if data is None:
        return None

    # Detect format
    if "openapi" in data and data["openapi"].startswith("3"):
        return _parse_openapi3(data)
    if "swagger" in data and data["swagger"].startswith("2"):
        return _parse_swagger2(data)
    if "info" in data and "item" in data:
        return _parse_postman(data)

    logger.warning("Unknown spec format in %s — expected OpenAPI 2/3 or Postman collection", path)
    return None


def _parse_openapi3(data: Dict) -> ApiSpec:
    info = data.get("info", {})
    servers = data.get("servers", [{}])
    base_url = servers[0].get("url", "") if servers else ""

    spec = ApiSpec(
        title=info.get("title", "Unknown API"),
        version=info.get("version", ""),
        base_url=base_url,
        spec_format="openapi3",
    )

    # Security schemes
    components = data.get("components", {})
    for scheme_name in components.get("securitySchemes", {}).keys():
        spec.security_schemes.append(scheme_name)

    # Endpoints
    global_security = bool(data.get("security"))
    for path_str, path_item in data.get("paths", {}).items():
        for method in ("get", "post", "put", "patch", "delete", "head", "options"):
            operation = path_item.get(method)
            if operation is None:
                continue
            requires_auth = bool(operation.get("security") or global_security)
            endpoint = ApiEndpoint(
                method=method.upper(),
                path=path_str,
                summary=operation.get("summary", ""),
                requires_auth=requires_auth,
                tags=operation.get("tags", []),
                operation_id=operation.get("operationId", ""),
            )
            # Parameters
            endpoint.parameters = operation.get("parameters", path_item.get("parameters", []))
            # Request body
            req_body = operation.get("requestBody", {})
            content = req_body.get("content", {})
            for media_type, media_data in content.items():
                endpoint.request_body_schema = media_data.get("schema")
                break
            # Response schemas
            for status_code, resp in operation.get("responses", {}).items():
                resp_content = resp.get("content", {})
                for media_type, media_data in resp_content.items():
                    endpoint.response_schemas[status_code] = media_data.get("schema", {})
                    break
            spec.endpoints.append(endpoint)

    return spec


def _parse_swagger2(data: Dict) -> ApiSpec:
    info = data.get("info", {})
    host = data.get("host", "")
    base_path = data.get("basePath", "/")
    schemes = data.get("schemes", ["https"])
    base_url = f"{schemes[0]}://{host}{base_path}" if host else base_path

    spec = ApiSpec(
        title=info.get("title", "Unknown API"),
        version=info.get("version", ""),
        base_url=base_url,
        spec_format="swagger2",
    )

    global_security = bool(data.get("security"))
    for path_str, path_item in data.get("paths", {}).items():
        for method in ("get", "post", "put", "patch", "delete", "head", "options"):
            operation = path_item.get(method)
            if operation is None:
                continue
            requires_auth = bool(operation.get("security") or global_security)
            endpoint = ApiEndpoint(
                method=method.upper(),
                path=path_str,
                summary=operation.get("summary", ""),
                requires_auth=requires_auth,
                tags=operation.get("tags", []),
                operation_id=operation.get("operationId", ""),
                parameters=operation.get("parameters", []),
            )
            spec.endpoints.append(endpoint)

    return spec


def _parse_postman(data: Dict) -> ApiSpec:
    info = data.get("info", {})
    spec = ApiSpec(
        title=info.get("name", "Unknown Collection"),
        version=info.get("schema", ""),
        base_url="",
        spec_format="postman",
    )

    def _extract_items(items, prefix=""):
        for item in items:
            if "item" in item:
                _extract_items(item["item"], prefix + item.get("name", "") + "/")
            elif "request" in item:
                req = item["request"]
                method = req.get("method", "GET").upper()
                url = req.get("url", {})
                path = "/" + "/".join(url.get("path", [])) if isinstance(url, dict) else str(url)
                endpoint = ApiEndpoint(
                    method=method,
                    path=path,
                    summary=item.get("name", ""),
                )
                spec.endpoints.append(endpoint)

    _extract_items(data.get("item", []))
    return spec

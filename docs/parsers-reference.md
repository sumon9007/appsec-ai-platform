# Parsers Reference

## Parser Summary

| Parser | What It Extracts | Used By |
|--------|------------------|---------|
| `cookie_parser.py` | Cookie flags and attributes | Cookie audit |
| `html_parser.py` | Links, forms, scripts, iframes, comments | Crawler, input validation audit |
| `jwt_parser.py` | JWT header/payload metadata and risk hints | Session/JWT audit |
| `manifest.py` | Dependency package lists from common ecosystems | Dependency audit |
| `openapi_parser.py` | API endpoint inventory from OpenAPI/Swagger/Postman | API audit |

## Notes

### Cookie Parser

- Produces `ParsedCookie`
- Identifies likely session cookies by name heuristic
- Does not perform any network activity

### HTML Parser

- Prefers BeautifulSoup when installed
- Falls back to regex parsing if unavailable
- Produces `PageInventory` and `HtmlForm` objects

### JWT Parser

- Decodes without signature verification
- Flags `alg:none`, weak algorithms, expiry state, and sensitive claims
- Truncates stored raw token representation for safety

### Manifest Parser

- Supports Python, npm, Go, RubyGems, Packagist, and basic Maven parsing
- Returns tuples of `(package, version, ecosystem)`

### OpenAPI Parser

- Supports OpenAPI 3, Swagger 2, and Postman collections
- Extracts endpoint list, auth hints, parameters, and schemas where available

Needs verification:
- Postman parsing is more lightweight than the OpenAPI paths and does not model the same level of detail.

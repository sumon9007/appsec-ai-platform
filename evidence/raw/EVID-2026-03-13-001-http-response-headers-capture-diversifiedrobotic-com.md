# Evidence: EVID-2026-03-13-001

**Label:** EVID-2026-03-13-001
**Date Collected:** 2026-03-13
**Collector:** Codex workspace runner
**Type:** HTTP Capture
**Domain:** Security Headers
**Related Finding:** PENDING

---

## Description

HTTP response headers capture — diversifiedrobotic.com

---

## Evidence Content

```
Request URL: https://diversifiedrobotic.com/
Final URL: https://diversifiedrobotic.com/
Status: 200

Redirect Chain:
No redirects

Response Headers:
Content-Type: text/html; charset=utf-8
Date: Fri, 13 Mar 2026 07:21:04 GMT
Cache-Control: no-store, no-cache, must-revalidate
Content-Encoding: gzip
ETag: "147yt8fgkqat35"
Transfer-Encoding: chunked
Vary: RSC, Next-Router-State-Tree, Next-Router-Prefetch, Next-Router-Segment-Prefetch, Accept-Encoding
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
request-context: appId=cid-v1:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: no-referrer
X-XSS-Protection: 1; mode=block
x-nextjs-cache: HIT
x-nextjs-prerender: 1
x-nextjs-stale-time: 4294967294
X-Powered-By: Next.js
```

---

## Observations

Full response headers captured from https://diversifiedrobotic.com/ for security header analysis. Status: 200. Redirects: 0.

---

## Chain of Custody Notes

Collected automatically by appsec-audit-tool. Target: https://diversifiedrobotic.com/.
No sensitive data redactions applied.

# Evidence: EVID-2026-03-13-002

**Label:** EVID-2026-03-13-002
**Date Collected:** 2026-03-13
**Collector:** Codex workspace runner
**Type:** Tool Output
**Domain:** TLS / Certificate
**Related Finding:** PENDING

---

## Description

TLS certificate and protocol details — diversifiedrobotic.com

---

## Evidence Content

```
Host: diversifiedrobotic.com:443
Negotiated Protocol: TLSv1.3
Cipher Suite: TLS_AES_256_GCM_SHA384 (bits: 256)

Certificate Subject CN: diversifiedrobotic.com
Subject Alternative Names:
  DNS: diversifiedrobotic.com

Issuer: GeoTrust TLS RSA CA G1 (DigiCert Inc)
Valid From: Feb 18 00:00:00 2026 GMT
Valid Until: Aug 18 23:59:59 2026 GMT
Days to Expiry: 158
Signature Algorithm: unknown

[REVIEW GAP] Cipher suite enumeration requires authorized active TLS scanning (e.g., testssl.sh or SSL Labs API). Only the negotiated cipher is shown above.
```

---

## Observations

TLS connection to diversifiedrobotic.com:443 successful. Protocol: TLSv1.3. Certificate expires: Aug 18 23:59:59 2026 GMT (158 days remaining).

---

## Chain of Custody Notes

Collected automatically by appsec-audit-tool. Target: https://diversifiedrobotic.com/.
No sensitive data redactions applied.

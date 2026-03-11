# Security Acceptance Criteria Checklist

This checklist maps audit findings and observations against defined security expectations.

The purpose is to track:

- visible control strengths
- visible weaknesses
- evidence gaps
- remediation priorities

---

## Acceptance Criteria Status

| Status | Meaning |
|------|--------|
| Met | Evidence supports control implementation |
| Partially Met | Control exists but is incomplete |
| Not Met | Evidence supports control failure |
| Review Gap | Evidence insufficient to determine |

---

## Criteria List

### AC-01 Secure Transport

Ensure HTTPS is consistently enforced and downgrade attacks are mitigated.

Status:  
Evidence:  
Notes:

---

### AC-02 Strong Authentication

Authentication mechanisms should protect accounts from unauthorized access.

Status:  
Evidence:  
Notes:

---

### AC-03 Browser Security Headers

Critical browser security headers should be present and properly configured.

Status:  
Evidence:  
Notes:

---

### AC-04 Session Security

Sessions should be protected against hijacking and misuse.

Status:  
Evidence:  
Notes:

---

### AC-05 Access Control

Users must only access resources permitted by their role.

Status:  
Evidence:  
Notes:

---

### AC-06 Input Validation

User input should be validated to prevent injection and unsafe processing.

Status:  
Evidence:  
Notes:

---

### AC-07 Security Logging

Security-relevant actions should be logged and reviewable.

Status:  
Evidence:  
Notes:

---

### AC-08 Dependency Security

Software components should be monitored for vulnerabilities.

Status:  
Evidence:  
Notes:

---

## Checklist Guidance

- Only mark **Not Met** if evidence clearly supports it.
- If visibility is limited, mark **Review Gap**.
- Use this checklist to guide remediation prioritization.
# Command: /generate-remediation-plan

Generate a prioritized remediation plan from the findings register, with owner fields, target dates, verification steps, and SLA alignment.

## Trigger

Invoked when the user wants to produce a formal remediation plan for tracked findings. Typically run after `/generate-report` or at the end of any audit cycle.

---

## Pre-Conditions

1. Findings register is populated with at least one open finding
2. `.claude/docs/remediation-standard.md` has been read
3. `.claude/context/audit-context.md` is populated for engagement metadata

---

## Steps

### Step 1: Load Report Writer Skill

Load: `.claude/skills/report-writer/SKILL.md`

Read:
- `.claude/skills/report-writer/templates/remediation-plan-template.md`
- `.claude/docs/remediation-standard.md`
- `.claude/rules/remediation-rules.md`

### Step 2: Read Findings Register

1. Read the current findings register
2. Filter to open and in-progress findings (exclude Closed findings)
3. Also note any "Risk Accepted" findings (include in plan with risk acceptance noted)

### Step 3: Prioritize by Severity and SLA

Sort findings using the following priority order:

1. **Critical** — SLA: 24 hours — top of plan, immediate action column
2. **High** — SLA: 7 days — second section
3. **Medium** — SLA: 30 days — third section
4. **Low** — SLA: 90 days — fourth section
5. **Info** — Next cycle — reference section

Within each severity tier, further sort by:
- Age of finding (oldest first — most at-risk for SLA breach)
- Domain (group related findings for efficiency)

### Step 4: Calculate SLA Deadlines

For each finding:
- Find Date: date the finding was identified
- SLA Duration: per severity (Critical 1d, High 7d, Medium 30d, Low 90d)
- SLA Deadline: Find Date + SLA Duration
- Days Overdue: if SLA Deadline < today → calculate days overdue (flag in red/bold)
- Days Remaining: if SLA Deadline ≥ today → calculate days remaining

### Step 5: Assign Remediation Actions

For each finding, document:
- **Action Required:** What specifically needs to be done (derived from the finding's Recommendation field)
- **Owner:** [PLACEHOLDER — assign to responsible team/individual]
- **Target Date:** SLA deadline (or earlier if overdue)
- **Verification Method:** How will the fix be confirmed? (Re-test, code review, configuration check)
- **Status:** Open / In Progress / Risk Accepted

### Step 6: Populate Remediation Plan Template

Using `remediation-plan-template.md`:

1. Populate the plan header: engagement name, date generated, total findings count
2. Populate the Critical findings table
3. Populate the High findings table
4. Populate the Medium findings table
5. Populate the Low/Info findings table
6. Add a summary statistics section: findings by severity, overdue findings, upcoming SLA deadlines

### Step 7: Special Handling

#### Overdue Findings
- Highlight any finding past its SLA deadline
- Note whether a risk acceptance is on file
- Recommend escalation path if no risk acceptance exists

#### Findings with No Fix Available
- If a dependency CVE has no fix, document:
  - Interim mitigating control (e.g., WAF rule, feature disable)
  - Monitoring for fix release
  - Risk acceptance justification

#### Grouped Remediations
- If multiple findings share the same root cause, group them with a single remediation action
- Note the grouped Finding IDs

### Step 8: Save and Distribute

1. Save to: `reports/draft/YYYY-MM-DD-[type]-remediation-plan.md`
2. After review, promote to `reports/final/`
3. Share with development team for owner assignment
4. Set a calendar reminder to verify SLA deadline compliance

---

## Outputs

| Output | Location | Template |
|--------|----------|---------|
| Remediation plan (draft) | `reports/draft/YYYY-MM-DD-[type]-remediation-plan.md` | `remediation-plan-template.md` |

---

## Related Commands

- `/generate-report` — Generate full security reports (companion command)
- `/audit-release` — Release gate uses remediation plan status to make pass/fail decision

# ITR-002 — ARTIFACT SELECTION GATE

A candidate artifact is admissible only if every mandatory condition is satisfied.

| Gate | Requirement | Status |
|---|---|---|
| G-001 | Third-party authorship | HOLD |
| G-002 | No reviewer contribution | HOLD |
| G-003 | Public repository | HOLD |
| G-004 | Exact baseline version available | HOLD |
| G-005 | Exact candidate version available | HOLD |
| G-006 | Documented technical change or remediation | HOLD |
| G-007 | Same verifier can run against both versions | HOLD |
| G-008 | Bounded executable surface | HOLD |
| G-009 | Implementation and tests inspectable | HOLD |
| G-010 | Independent adversarial extensions possible | HOLD |
| G-011 | Review can be completed without privileged access | HOLD |
| G-012 | Consequence and scope are proportionate | HOLD |

## Admission rule

Artifact admission requires all mandatory gates to be classified PASS.

Any unresolved authorship, version, reproducibility, or contribution condition remains HOLD.

No artifact is admitted merely because it is popular, important, or technically complex.
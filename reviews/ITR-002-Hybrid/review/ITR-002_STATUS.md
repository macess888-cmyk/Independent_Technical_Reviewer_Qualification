# ITR-002 - STATUS

**Status:** HYBRID REVIEW EXECUTION COMPLETE - FINAL REVIEW PENDING

## Review identity

**Review ID:** ITR-002  
**Reviewer:** Jake Macdonald  
**Review type:** Hybrid differential and adversarial review

## Admitted artifact

- Artifact: urllib3
- Repository: https://github.com/urllib3/urllib3
- Advisory: GHSA-v845-jxx5-vc9f
- Baseline release: 2.0.5
- Baseline commit: `d9f85a749488188c286cd50606d159874db94d5f`
- Candidate release: 2.0.6
- Candidate commit: `262e3e332209ee93ff70e2b13502c8f20c105ac8`

## Bounded claim

When urllib3 follows a cross-origin redirect, version 2.0.6 removes a caller-supplied `Cookie` header before sending the redirected request, whereas version 2.0.5 forwards it.

## Admission result

All twelve mandatory artifact-selection gates are classified PASS.

**Artifact admission:** PASS

## Differential result

The same directly runnable verifier executed successfully against both exact releases.

### Baseline 2.0.5

- process exit code: `0`
- HTTP response status: `200`
- Cookie forwarded: `true`
- unrelated control header preserved: `true`

### Candidate 2.0.6

- process exit code: `0`
- HTTP response status: `200`
- Cookie forwarded: `false`
- unrelated control header preserved: `true`

**Baseline discrimination:** PASS  
**Candidate confirmation:** PASS  
**Differential proof:** PASS  
**Reproducible carrier:** PASS

## Adversarial execution result

The same adversarial matrix executed against both exact releases.

### Baseline 2.0.5

- case count: `15`
- passed: `15`
- failed: `0`
- process exit code: `0`
- overall classification: `PASS`

### Candidate 2.0.6

- case count: `15`
- passed: `15`
- failed: `0`
- process exit code: `0`
- overall classification: `PASS`

No failed adversarial cases were returned for either version.

## Adversarial dimensions executed

The matrix exercised:

- 301 redirect;
- 302 redirect;
- 303 redirect;
- 307 redirect;
- 308 redirect;
- mixed-case Cookie header;
- same-origin redirect controls;
- cross-origin redirect behavior;
- hostname change;
- port change;
- multiple redirect hops;
- redirects disabled;
- empty Cookie value;
- unrelated-header preservation;
- Authorization-header comparison;
- explicit `remove_headers_on_redirect` override behavior.

## Current classifications

| Dimension | Classification |
|---|---|
| Third-party independence | PASS |
| Frozen baseline identity | PASS |
| Frozen candidate identity | PASS |
| Artifact admission | PASS |
| Claim confirmation | PASS |
| Baseline discrimination | PASS |
| Differential proof | PASS |
| Reproducible carrier | PASS |
| Adversarial challenge | PASS |
| Final hybrid determination | PASS |

## Evidence completed

- repository identity preserved;
- baseline and candidate tags verified;
- baseline and candidate commits preserved;
- reviewer contribution searches preserved;
- source differential preserved;
- upstream test differential preserved;
- exact package versions installed separately;
- identical differential probe executed against both versions;
- baseline differential output preserved;
- candidate differential output preserved;
- differential process exit codes preserved;
- artifact-selection gate completed;
- manifest updated;
- adversarial matrix authored;
- adversarial matrix executed against both versions;
- machine-readable adversarial results preserved;
- adversarial summary outputs preserved;
- adversarial process exit codes preserved;
- failed-case inspection returned no failed cases.

## Final review work pending

The technical execution phase is complete.

The following publication work remains:

- issue the final ITR-002 independent technical review;
- create the final claim-to-evidence ledger;
- state limitations and prohibited promotions;
- hash the final review;
- preserve an evidence inventory;
- commit and freeze the completed ITR-002 package.

## Final determination boundary

The present PASS establishes only that:

- the documented Cookie-removal change is observable between urllib3 2.0.5 and 2.0.6;
- the same verifier distinguishes the vulnerable baseline from the fixed candidate;
- the tested adversarial and control variations behaved as expected;
- the carrier is directly runnable in the preserved environment.

It does not establish:

- complete urllib3 security;
- complete redirect security;
- comprehensive SSRF protection;
- absence of unrelated vulnerabilities;
- correctness across all platforms and Python versions;
- qualification across unrelated artifact classes;
- full adversarial security-review qualification.

## Next permitted action

Issue the final bounded ITR-002 review without altering the frozen baseline, candidate, differential evidence, or adversarial evidence.

## Current final status

**Artifact admitted:** YES  
**Differential proof complete:** YES  
**Adversarial phase complete:** YES  
**Final review issued:** NO  
**Current overall classification:** PASS
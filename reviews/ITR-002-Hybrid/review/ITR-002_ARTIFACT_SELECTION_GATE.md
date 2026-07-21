# ITR-002 - ARTIFACT SELECTION GATE

## Candidate

**Artifact:** urllib3  
**Repository:** https://github.com/urllib3/urllib3  
**Advisory:** GHSA-v845-jxx5-vc9f  
**Baseline release:** 2.0.5  
**Baseline commit:** `d9f85a749488188c286cd50606d159874db94d5f`  
**Candidate release:** 2.0.6  
**Candidate commit:** `262e3e332209ee93ff70e2b13502c8f20c105ac8`

## Gate assessment

| Gate | Requirement | Status |
|---|---|---|
| G-001 | Third-party authorship | PASS |
| G-002 | No reviewer contribution | PASS |
| G-003 | Public repository | PASS |
| G-004 | Exact baseline version available | PASS |
| G-005 | Exact candidate version available | PASS |
| G-006 | Documented technical change or remediation | PASS |
| G-007 | Same verifier can run against both versions | PASS |
| G-008 | Bounded executable surface | PASS |
| G-009 | Implementation and tests inspectable | PASS |
| G-010 | Independent adversarial extensions possible | PASS |
| G-011 | Review can be completed without privileged access | PASS |
| G-012 | Consequence and scope are proportionate | PASS |

## Evidence supporting admission

### Independence

The artifact, repository, implementation, advisory, release scope, baseline, candidate, and technical claim were not authored, owned, maintained, or controlled by Jake Macdonald.

Repository history searches for:

- `Jake Macdonald`
- `Macess888@gmail.com`

returned no matching commits.

### Frozen carriers

The exact releases and commits were verified:

```text
Baseline 2.0.5
d9f85a749488188c286cd50606d159874db94d5f

Candidate 2.0.6
262e3e332209ee93ff70e2b13502c8f20c105ac8
`h`

### Documented remediation

The source differential changed the default redirect-removal set from:

```text
Authorization
```

to:

```text
Cookie
Authorization
```

The upstream test differential added coverage for:

- default Cookie removal;
- mixed-case Cookie handling;
- explicit removal-policy overrides;
- preservation when removal is disabled.

### Same-verifier differential

The same directly runnable probe executed successfully against both exact releases.

#### Baseline 2.0.5

- process exit code: `0`
- HTTP response status: `200`
- Cookie forwarded to redirected origin: `true`
- unrelated control header preserved: `true`

#### Candidate 2.0.6

- process exit code: `0`
- HTTP response status: `200`
- Cookie forwarded to redirected origin: `false`
- unrelated control header preserved: `true`

This establishes observable fail-before/pass-after separation using the same executable carrier.

## Bounded review claim

When urllib3 follows a cross-origin redirect, version 2.0.6 removes a caller-supplied `Cookie` header before sending the redirected request, whereas version 2.0.5 preserves the vulnerable behavior.

## Planned adversarial extensions

The admitted artifact supports independent testing of:

- 301 redirects;
- 302 redirects;
- 303 redirects;
- 307 redirects;
- 308 redirects;
- mixed-case Cookie headers;
- same-origin redirects;
- hostname changes;
- port changes;
- multiple redirect hops;
- redirects disabled;
- empty Cookie values;
- unrelated-header preservation;
- Authorization-header comparison;
- explicit `remove_headers_on_redirect` overrides.

## Admission decision

##Artifact admission: PASS**

urllib3 versions 2.0.5 and 2.0.6 are admitted as the frozen baseline and candidate carriers for ITR-002.

All twelve mandatory gates are satisfied.

The next permitted phase is independently originated adversarial test design and execution.

## Prohibited promotion

Artifact admission does not establish:

- complete urllib3 security;
- complete redirect security;
- comprehensive SSRF protection;
- absence of unrelated vulnerabilities;
- qualification across unrelated artifact classes;
- full adversarial security-review qualification.

Those conclusions remain outside the current evidence boundary.

# ITR-002 — CANDIDATE ASSESSMENT

## Candidate

**Artifact:** urllib3  
**Repository:** https://github.com/urllib3/urllib3  
**Advisory:** GHSA-v845-jxx5-vc9f  
**Baseline release:** 2.0.5  
**Baseline commit:** `d9f85a749488188c286cd50606d159874db94d5f`  
**Candidate release:** 2.0.6  
**Candidate commit:** `262e3e332209ee93ff70e2b13502c8f20c105ac8`

## Proposed bounded claim

When urllib3 follows a cross-origin redirect, version 2.0.6 removes a caller-supplied `Cookie` header before sending the redirected request, whereas version 2.0.5 preserves the vulnerable behavior.

## Reviewer independence

The artifact, design, implementation, advisory, release scope, baseline, candidate, and technical claim were not authored or controlled by Jake Macdonald.

Repository history searches for:

- `Jake Macdonald`
- `Macess888@gmail.com`

returned no matching commits.

## Differential expectation

### Baseline 2.0.5

A caller-supplied `Cookie` header is forwarded to a different redirect origin.

### Candidate 2.0.6

The `Cookie` header is stripped before the cross-origin redirected request.

## Planned confirmation tests

- cross-origin redirect strips Cookie;
- same-origin redirect preserves Cookie where intended;
- HTTP and HTTPS behavior remain bounded to the configured test environment.

## Planned differential tests

The same harness will run against both exact releases:

- 2.0.5 must expose the vulnerable behavior;
- 2.0.6 must exhibit the fixed behavior.

## Planned adversarial extensions

- mixed-case `Cookie` header;
- 301 redirect;
- 302 redirect;
- 303 redirect;
- 307 redirect;
- 308 redirect;
- hostname change;
- port change;
- multi-hop redirect;
- redirects disabled;
- empty Cookie value;
- unrelated header preservation;
- Authorization-header comparison;
- same-origin control.

## Current classification

**Artifact admission: HOLD**

Reason:

The same directly runnable verifier has not yet been executed successfully against both frozen releases.

## Remaining gate

**G-007 — Same verifier can run against baseline and candidate: HOLD**
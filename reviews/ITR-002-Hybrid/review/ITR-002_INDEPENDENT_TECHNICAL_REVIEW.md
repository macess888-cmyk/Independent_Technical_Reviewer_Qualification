# INDEPENDENT TECHNICAL REVIEW 002

## urllib3 2.0.6 Cross-Origin Cookie Redirect Remediation

**Review ID:** ITR-002  
**Reviewer:** Jake Macdonald  
**Review date:** 2026-07-20  
**Review type:** Hybrid differential and adversarial review  
**Artifact:** urllib3  
**Advisory:** GHSA-v845-jxx5-vc9f

## 1. Executive conclusion

Within the frozen review boundary, the documented urllib3 Cookie-header redirect remediation is classified **PASS**.

The same directly runnable verifier demonstrated:

- vulnerable behavior in urllib3 2.0.5;
- fixed behavior in urllib3 2.0.6;
- fail-before/pass-after discrimination;
- preservation of unrelated control headers;
- successful execution of an independently authored adversarial matrix against both versions.

The baseline and candidate adversarial matrices each executed 15 cases:

```text
urllib3 2.0.5
Executed: 15
Passed: 15
Failed: 0

urllib3 2.0.6
Executed: 15
Passed: 15
Failed: 0
```

The PASS classification is bounded to the documented cross-origin Cookie-header redirect behavior and the executed variations.

This review does not establish complete urllib3 security, complete redirect security, comprehensive SSRF protection, or absence of unrelated vulnerabilities.

## 2. Reviewer independence

The reviewer did not:

- author urllib3;
- maintain the urllib3 repository;
- design the reviewed remediation;
- author the advisory;
- define the release scope;
- contribute to either frozen release;
- author the upstream claim;
- control the baseline or candidate artifacts.

Repository-history searches for:

```text
Jake Macdonald
Macess888@gmail.com
```

returned no matching commits.

Reviewer-authored verification code was stored outside the third-party repository.

## 3. Frozen carriers

### Baseline

**Version:** 2.0.5  
**Commit:**

```text
d9f85a749488188c286cd50606d159874db94d5f
```

### Candidate

**Version:** 2.0.6  
**Commit:**

```text
262e3e332209ee93ff70e2b13502c8f20c105ac8
```

The cloned source repository was inspected in detached HEAD state.

The baseline and candidate Python packages were installed into separate local target directories.

## 4. Bounded claim

When urllib3 follows a cross-origin redirect, version 2.0.6 removes a caller-supplied `Cookie` header before sending the redirected request, whereas version 2.0.5 forwards it.

## 5. Review boundary

### Included

- exact urllib3 2.0.5 baseline;
- exact urllib3 2.0.6 candidate;
- GHSA-v845-jxx5-vc9f remediation claim;
- source differential;
- upstream test differential;
- isolated installation of both versions;
- same-verifier differential execution;
- independently authored adversarial variations;
- machine-readable results;
- PASS / PARTIAL / FAIL / HOLD classification.

### Excluded

- complete urllib3 security;
- comprehensive HTTP client security;
- comprehensive redirect security;
- comprehensive SSRF protection;
- undisclosed vulnerabilities;
- proxy-specific assurance beyond executed paths;
- TLS and certificate validation assurance;
- deployment-specific controls;
- correctness across every Python version and operating system;
- qualification across unrelated artifact classes.

## 6. Source differential

The default redirect-removal set changed from:

```text
Authorization
```

in urllib3 2.0.5 to:

```text
Cookie
Authorization
```

in urllib3 2.0.6.

The implementation continued to remove configured headers when the redirected destination was not the same host.

The relevant behavior remained configurable through `remove_headers_on_redirect`.

## 7. Upstream test differential

The upstream test changes added or expanded coverage for:

- default Cookie removal;
- mixed-case Cookie handling;
- cross-origin redirect behavior;
- explicit empty removal-policy overrides;
- preservation of Cookie when removal was intentionally disabled;
- preservation of Cookie when only another custom header was configured for removal.

The upstream tests support the interpretation that the remediation added `Cookie` to the default cross-origin redirect-removal policy rather than prohibiting all Cookie forwarding unconditionally.

## 8. Direct differential execution

The same verifier was executed against both exact package versions.

### urllib3 2.0.5 observed result

```text
process exit code: 0
response status: 200
cookie_forwarded: true
control_header_preserved: true
```

The redirected destination received:

```text
Cookie: review_session=secret-value
X-Review-Control: preserve-me
```

### urllib3 2.0.6 observed result

```text
process exit code: 0
response status: 200
cookie_forwarded: false
control_header_preserved: true
```

The redirected destination did not receive the `Cookie` header.

It continued to receive:

```text
X-Review-Control: preserve-me
```

### Differential classification

| Dimension | Result |
|---|---|
| Baseline exhibits vulnerable behavior | PASS |
| Candidate exhibits fixed behavior | PASS |
| Same verifier executed against both versions | PASS |
| Unrelated control header preserved | PASS |
| Fail-before/pass-after discrimination | PASS |

**Differential proof:** PASS

## 9. Adversarial matrix

The independently authored matrix exercised:

- redirect status 301;
- redirect status 302;
- redirect status 303;
- redirect status 307;
- redirect status 308;
- mixed-case `Cookie` header;
- same-origin redirect controls;
- cross-origin redirect behavior;
- hostname change;
- port change;
- multiple redirect hops;
- redirect-disabled control;
- empty Cookie value;
- unrelated-header preservation;
- Authorization-header comparison;
- explicit `remove_headers_on_redirect=[]` override.

## 10. Adversarial results

### urllib3 2.0.5

```text
case_count: 15
passed: 15
failed: 0
exit_code: 0
overall_classification: PASS
```

The matrix expected vulnerable baseline behavior where appropriate.

A PASS for the baseline does not mean the baseline is secure. It means the observed behavior matched the frozen baseline expectation for each case.

### urllib3 2.0.6

```text
case_count: 15
passed: 15
failed: 0
exit_code: 0
overall_classification: PASS
```

The matrix expected fixed candidate behavior where appropriate.

No failed cases were returned for either version.

## 11. Important controls

### Same-origin redirects

Cookie and Authorization headers remained available on same-origin redirects.

This supports the narrower conclusion that the remediation targets cross-origin forwarding rather than suppressing these headers for all redirects.

### Unrelated-header preservation

`X-Review-Control` remained present across the tested cross-origin redirects.

This supports the conclusion that the candidate did not indiscriminately remove all caller-supplied headers.

### Authorization comparison

Authorization behavior served as an established redirect-removal comparison.

### Removal-policy override

When `remove_headers_on_redirect=[]` was explicitly supplied, Cookie forwarding was preserved.

This is consistent with the behavior being a configurable default policy.

The security effect therefore depends on callers not explicitly disabling the removal policy.

### Redirect-disabled control

When redirects were disabled, no redirected destination request occurred.

## 12. Claim classification

| Review layer | Classification |
|---|---|
| Third-party independence | PASS |
| Baseline identity | PASS |
| Candidate identity | PASS |
| Artifact admission | PASS |
| Source remediation located | PASS |
| Upstream test evidence located | PASS |
| Candidate claim confirmation | PASS |
| Baseline discrimination | PASS |
| Differential proof | PASS |
| Reproducible carrier | PASS |
| Adversarial challenge | PASS |
| Final bounded determination | PASS |

## 13. Interpretation of baseline PASS

The baseline adversarial matrix reports PASS because each test evaluates whether the baseline exhibits its expected pre-remediation behavior.

For cross-origin cases, the expected baseline behavior includes forwarding the Cookie header.

Therefore:

```text
baseline test PASS
```

means:

```text
the verifier successfully observed the vulnerable baseline behavior
```

It does not mean:

```text
urllib3 2.0.5 is secure
```

## 14. Limitations

The verifier used local HTTP servers bound to loopback interfaces.

Cross-origin separation was created through combinations of:

- `localhost`;
- `127.0.0.1`;
- different listening ports.

The review did not execute public-network destinations.

The review did not establish:

- behavior through every proxy configuration;
- behavior under every TLS configuration;
- behavior across all urllib3 request APIs;
- behavior across all Python runtimes;
- behavior across all operating systems;
- comprehensive hostname normalization assurance;
- complete credential-leak prevention;
- comprehensive SSRF mitigation;
- absence of bypasses outside the tested header-removal path;
- absence of unrelated vulnerabilities.

The adversarial matrix broadened the executed boundary but remained focused on the documented remediation property.

## 15. Prohibited promotion

The evidence must not be promoted into any of the following claims:

- urllib3 is completely secure;
- all redirect behavior is secure;
- all Cookie handling is secure;
- all authorization handling is secure;
- SSRF is comprehensively prevented;
- no related bypass exists;
- all versions after 2.0.6 are automatically equivalent;
- the reviewer is qualified across every artifact class;
- one bounded review establishes general security-audit qualification.

## 16. Evidence package

The preserved evidence includes:

- baseline and candidate commit identities;
- reviewer-contribution searches;
- repository remote identity;
- clean source status;
- baseline source search;
- candidate source search;
- baseline upstream test search;
- candidate upstream test search;
- source differential;
- test differential;
- installed package-version records;
- baseline differential output;
- candidate differential output;
- differential exit codes;
- baseline adversarial summary;
- candidate adversarial summary;
- adversarial exit codes;
- machine-readable differential results;
- machine-readable adversarial results;
- artifact-selection gate;
- candidate assessment;
- manifest;
- verifier source;
- status record.

## 17. Final determination

Within the frozen review boundary:

```text
Artifact admission: PASS
Claim confirmation: PASS
Baseline discrimination: PASS
Differential proof: PASS
Adversarial challenge: PASS
Reproducible carrier: PASS
```

**Overall bounded determination: PASS**

The evidence supports the conclusion that urllib3 2.0.6 changed the default cross-origin redirect policy so that caller-supplied Cookie headers are removed, while urllib3 2.0.5 exhibits the earlier forwarding behavior.

This determination remains limited to the reviewed claim, frozen versions, executed carrier, and stated limitations.
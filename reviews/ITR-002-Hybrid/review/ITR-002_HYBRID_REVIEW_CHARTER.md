# ITR-002 — HYBRID DIFFERENTIAL AND ADVERSARIAL REVIEW CHARTER

**Review ID:** ITR-002  
**Reviewer:** Jake Macdonald  
**Status:** Artifact selection pending

## Objective

Demonstrate independent review capability through a hybrid method combining:

1. bounded release-claim verification;
2. fail-before/pass-after differential testing;
3. independently originated adversarial challenge;
4. directly runnable third-party verification;
5. machine-readable evidence;
6. proportional PASS / PARTIAL / FAIL / HOLD conclusions.

## Independence requirements

The reviewed artifact, claims, design, implementation, release scope, and remediation history must not be authored, owned, designed, maintained, or contributed to by Jake Macdonald.

## Required artifact properties

The selected artifact must provide:

- a public repository;
- a known earlier baseline;
- a later candidate or fixed release;
- one or more technically consequential claims;
- an executable and bounded surface;
- reproducible installation;
- inspectable implementation;
- no prior contribution by the reviewer.

## Review layers

### Layer 1 — Claim confirmation

Determine whether the candidate behaves as claimed.

### Layer 2 — Baseline discrimination

Run the same test against the earlier baseline.

### Layer 3 — Differential proof

Require observable fail-before/pass-after separation.

### Layer 4 — Adversarial challenge

Run independently originated challenges beyond direct release-note confirmation.

### Layer 5 — Reproducible carrier

Provide one directly runnable verifier that records identities, commands, outcomes, classifications, and limitations.

## Classification vocabulary

- PASS — evidence supports the bounded claim.
- PARTIAL — evidence supports only part of the claim or a narrower condition.
- FAIL — evidence contradicts the claim.
- HOLD — evidence is unavailable, incomplete, or cannot yet be distinguished.

## Prohibited promotions

The review must not promote:

- candidate success without baseline discrimination into differential proof;
- release-note confirmation into broad adversarial assurance;
- passing tests into complete correctness;
- unavailable evidence into failure;
- one artifact class into general reviewer qualification.
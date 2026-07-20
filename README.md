# Independent Technical Reviewer Qualification

This repository contains evidence-based independent technical reviews of third-party artifacts.

## Review 001

**Artifact:** PyJWT 2.13.0  
**Review ID:** ITR-001  
**Frozen commit:** `7144e4534c34810f4525dc4578a32addd8212cff`  
**Overall bounded determination:** PASS  
**Complete upstream matrix reproduction:** HOLD

The review evaluates five security behaviours explicitly claimed in the PyJWT 2.13.0 release notes.

Each claim was assessed through:

- frozen source inspection;
- upstream test inspection;
- independent CPython 3.12 reproduction;
- reviewer-authored counterexamples;
- preserved evidence and cryptographic hashes.

## Principal review artifact

`reviews/ITR-001-PyJWT/review/ITR-001_INDEPENDENT_TECHNICAL_REVIEW.md`

## Supporting records

- Review boundary
- Reproduction record
- Claim-to-evidence ledger
- Reviewer-authored test suite
- Execution records
- Source and test extracts
- SHA-256 receipts
- Evidence inventory

## Review limitations

This review does not claim:

- complete security assurance;
- formal verification;
- full upstream CI reproduction;
- compatibility across unavailable Python and PyPy interpreters;
- absence of unrelated or undisclosed vulnerabilities.

Unknown or unreproduced conditions remain classified HOLD.
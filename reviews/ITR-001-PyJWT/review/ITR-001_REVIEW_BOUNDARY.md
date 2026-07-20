# ITR-001 - REVIEW BOUNDARY

Review ID: ITR-001
Artifact: PyJWT 2.13.0
Frozen commit: 7144e4534c34810f4525dc4578a32addd8212cff
Reviewer: Jake Macdonald
Review date: 2026-07-20

## Review question

Does PyJWT 2.13.0 implement and test the five security behaviours explicitly stated in its release changelog?

## Included claims

C-001: Reject JWK JSON documents supplied as raw HMAC secrets.
C-002: Bind JWT header alg to PyJWK.algorithm_name during verification.
C-003: Reject non-http and non-https URI schemes in PyJWKClient.
C-004: Preserve the cached JWK Set when fetching a replacement fails.
C-005: Correctly process b64=false detached compact payloads without unconditional base64 decoding.

## Included evidence

Frozen source implementation.
Frozen upstream tests.
Independent CPython 3.12 crypto and non-crypto test execution.
Reviewer-authored focused counterexamples.

## Excluded conclusions

No claim of complete security.
No claim of formal verification.
No claim of full upstream CI reproduction.
No claim covering unavailable Python or PyPy interpreters.
No claim covering undisclosed vulnerabilities.
No deployment-specific assurance.

## Classification vocabulary

PASS: claim supported by inspectable implementation and reproduced evidence.
PARTIAL: claim supported only in part or under narrower conditions.
FAIL: evidence directly contradicts the claim.
HOLD: evidence is unavailable, incomplete, or cannot yet be distinguished.

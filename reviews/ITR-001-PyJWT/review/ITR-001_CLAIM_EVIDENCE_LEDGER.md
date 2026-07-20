# ITR-001 - CLAIM TO EVIDENCE LEDGER

| ID | Release claim | Implementation | Upstream tests | Independent counterexample | Status |
|---|---|---|---|---|---|
| C-001 | Reject JWK JSON as HMAC secret | Located and inspected | Located and reproduced | Reviewer rejection and normal-secret control passed | PASS |
| C-002 | Bind header alg to PyJWK algorithm | Located and inspected | Located and reproduced | Mismatched algorithm rejected | PASS |
| C-003 | Reject non-HTTP and non-HTTPS JWKS URI schemes | Located and inspected | Located and reproduced | file, ftp, data, ldap and local path rejected; HTTP and HTTPS accepted | PASS |
| C-004 | Preserve cached JWK Set after fetch errors | Located and inspected | Located and reproduced | Cached set remained after simulated network failure | PASS |
| C-005 | Enforce b64=false detached-payload handling | Located and inspected | Located and reproduced | Non-empty compact segment and missing crit declaration rejected | PASS |

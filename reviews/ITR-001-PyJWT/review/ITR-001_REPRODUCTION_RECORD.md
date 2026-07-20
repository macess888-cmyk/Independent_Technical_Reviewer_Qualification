# ITR-001 - INDEPENDENT REPRODUCTION RECORD

Review ID: ITR-001
Artifact: PyJWT
Release: 2.13.0
Commit: 7144e4534c34810f4525dc4578a32addd8212cff
Reviewer: Jake Macdonald
Review date: 2026-07-20

## Independence

The reviewer did not author, design, scope, own, or contribute to the reviewed artifact.

## Frozen carrier

Repository: https://github.com/jpadilla/pyjwt.git
Tag: 2.13.0
Commit: 7144e4534c34810f4525dc4578a32addd8212cff
Checkout state: Detached HEAD
Source status before execution: Clean
Source status after execution: Clean

## Execution environment

Operating system: Microsoft Windows 10.0.26200.8875
Python: CPython 3.12.8
tox: 4.57.1

## Results

Full declared tox matrix: HOLD
Reason: The local environment does not contain every required CPython and PyPy interpreter.

Supported local matrix: PASS
typing: PASS
py312-crypto: PASS
py312-nocrypto: PASS
py312-mypy: PASS
py312-crypto-mypy: PASS

Lint: HOLD
Reason: The lint environment requires Python 3.10, which is unavailable locally.

## Prohibited promotion

This review does not claim reproduction across Python 3.9, 3.10, 3.11, 3.13, 3.14, or PyPy.
It does not claim that the complete upstream CI matrix was reproduced.
It does not classify unavailable interpreter lanes as product failures.

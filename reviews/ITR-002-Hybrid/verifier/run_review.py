from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal


Classification = Literal["PASS", "PARTIAL", "FAIL", "HOLD"]


@dataclass(frozen=True)
class ReviewResult:
    claim_id: str
    baseline_result: Classification
    candidate_result: Classification
    differential_result: Classification
    adversarial_result: Classification
    reproducibility_result: Classification
    overall_classification: Classification
    observations: tuple[str, ...]
    limitations: tuple[str, ...]


ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
MANIFEST_PATH = ROOT / "manifest.json"


def load_manifest() -> dict:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Missing manifest: {MANIFEST_PATH}")

    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_ready(manifest: dict) -> None:
    artifact = manifest.get("artifact", {})
    required = (
        "name",
        "repository",
        "baseline_version",
        "baseline_commit",
        "candidate_version",
        "candidate_commit",
    )

    missing = [field for field in required if not artifact.get(field)]
    if missing:
        raise RuntimeError(
            "Artifact selection remains HOLD. Missing manifest fields: "
            + ", ".join(missing)
        )


def run_review() -> list[ReviewResult]:
    manifest = load_manifest()
    validate_ready(manifest)

    raise NotImplementedError(
        "Artifact-specific confirmation, differential, and adversarial "
        "tests must be implemented after artifact admission."
    )


def write_results(results: list[ReviewResult]) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    destination = RESULTS_DIR / "review_results.json"

    payload = [asdict(result) for result in results]
    destination.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return destination


def main() -> int:
    try:
        results = run_review()
        destination = write_results(results)
    except (FileNotFoundError, RuntimeError, NotImplementedError) as exc:
        print(f"HOLD: {exc}")
        return 2
    except Exception as exc:
        print(f"FAIL: Unexpected verifier error: {type(exc).__name__}: {exc}")
        return 1

    print(f"PASS: Review results written to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    id: str
    category: str
    name: str
    passed: bool
    severity: str
    detail: str


CHECKS = (
    ("documentation", "quality", "README", "README.md", "medium", "Add a project README."),
    ("license", "legal", "License", "LICENSE", "high", "Add an open-source license."),
    ("gitignore", "quality", "Gitignore", ".gitignore", "medium", "Add a .gitignore file."),
    ("env-example", "security", "Environment template", ".env.example", "high", "Document required environment variables without committing secrets."),
    ("tests", "testing", "Tests", "tests", "high", "Add automated tests."),
    ("ci", "delivery", "CI", ".github/workflows", "high", "Add continuous integration."),
)


def run_checks(root: Path) -> list[Check]:
    checks: list[Check] = []
    for check_id, category, name, relative, severity, detail in CHECKS:
        exists = (root / relative).exists()
        checks.append(Check(check_id, category, name, exists, severity, "Present" if exists else detail))
    return checks


def score(checks: list[Check]) -> int:
    weights = {"high": 2, "medium": 1, "low": 1}
    total = sum(weights.get(c.severity, 1) for c in checks)
    earned = sum(weights.get(c.severity, 1) for c in checks if c.passed)
    return round(100 * earned / total) if total else 0


def result(root: Path) -> dict:
    checks = run_checks(root)
    return {
        "version": "0.2.0",
        "path": str(root.resolve()),
        "score": score(checks),
        "summary": {
            "passed": sum(c.passed for c in checks),
            "failed": sum(not c.passed for c in checks),
            "total": len(checks),
        },
        "checks": [asdict(c) for c in checks],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect practical repository engineering health.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to inspect")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    parser.add_argument("--min-score", type=int, metavar="N", help="Fail with exit code 2 when score is below N")
    args = parser.parse_args()

    root = Path(args.path).expanduser()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    data = result(root)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"RepoLens score: {data['score']}/100")
        for check in data["checks"]:
            marker = "PASS" if check["passed"] else "FAIL"
            print(f"[{marker}] {check['severity'].upper():6} {check['name']}: {check['detail']}")

    if args.min_score is not None and not 0 <= args.min_score <= 100:
        parser.error("--min-score must be between 0 and 100")
    if args.min_score is not None and data["score"] < args.min_score:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


CHECKS = (
    ("README", "README.md", "Add a project README."),
    ("License", "LICENSE", "Add an open-source license."),
    ("Gitignore", ".gitignore", "Add a .gitignore file."),
    ("Environment template", ".env.example", "Document required environment variables without secrets."),
    ("Tests", "tests", "Add automated tests."),
    ("CI", ".github/workflows", "Add continuous integration."),
)


def run_checks(root: Path) -> list[Check]:
    checks: list[Check] = []
    for name, relative, detail in CHECKS:
        exists = (root / relative).exists()
        checks.append(Check(name, exists, "Present" if exists else detail))
    return checks


def score(checks: list[Check]) -> int:
    return round(100 * sum(c.passed for c in checks) / len(checks)) if checks else 0


def result(root: Path) -> dict:
    checks = run_checks(root)
    return {
        "path": str(root.resolve()),
        "score": score(checks),
        "checks": [asdict(c) for c in checks],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect practical repository engineering hygiene.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to inspect")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    root = Path(args.path).expanduser()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    data = result(root)
    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    print(f"RepoLens score: {data['score']}/100")
    for check in data["checks"]:
        marker = "PASS" if check["passed"] else "FAIL"
        print(f"[{marker}] {check['name']}: {check['detail']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

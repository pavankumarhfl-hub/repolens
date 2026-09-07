from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

VERSION = "0.3.0"


@dataclass(frozen=True)
class Check:
    id: str
    category: str
    name: str
    passed: bool
    severity: str
    detail: str


@dataclass(frozen=True)
class Rule:
    id: str
    category: str
    name: str
    severity: str
    detail: str
    predicate: object


PROJECT_FILES = (
    "pyproject.toml", "package.json", "go.mod", "Cargo.toml", "pom.xml",
    "build.gradle", "build.gradle.kts", "composer.json", "Gemfile", "mix.exs",
)
LOCK_FILES = (
    "poetry.lock", "uv.lock", "Pipfile.lock", "package-lock.json", "npm-shrinkwrap.json",
    "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "go.sum", "Cargo.lock", "composer.lock",
)
SOURCE_DIRS = ("src", "app", "lib", "cmd", "packages")
TEST_DIRS = ("tests", "test", "spec")


def exists(root: Path, *paths: str) -> bool:
    return any((root / path).exists() for path in paths)


def nonempty_file(root: Path, path: str) -> bool:
    target = root / path
    return target.is_file() and target.stat().st_size > 0


def has_workflow(root: Path) -> bool:
    directory = root / ".github" / "workflows"
    return directory.is_dir() and any(p.suffix in {".yml", ".yaml"} for p in directory.iterdir())


def has_source(root: Path) -> bool:
    if exists(root, *SOURCE_DIRS):
        return True
    extensions = {".py", ".js", ".ts", ".tsx", ".go", ".rs", ".java", ".kt", ".c", ".cpp", ".cs", ".rb", ".php"}
    ignored = {".git", ".venv", "venv", "node_modules", "dist", "build"}
    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if path.is_file() and path.suffix in extensions:
            return True
    return False


def build_rules() -> tuple[Rule, ...]:
    return (
        Rule("documentation.readme", "documentation", "README", "medium", "Add a clear README.", lambda r: nonempty_file(r, "README.md")),
        Rule("legal.license", "legal", "License", "high", "Add an open-source license.", lambda r: exists(r, "LICENSE", "LICENSE.md", "LICENSE.txt")),
        Rule("quality.gitignore", "quality", "Gitignore", "medium", "Add a .gitignore file.", lambda r: nonempty_file(r, ".gitignore")),
        Rule("security.env-template", "security", "Environment template", "high", "Document configuration without committing secrets.", lambda r: nonempty_file(r, ".env.example", ".env.sample", "env.example")),
        Rule("testing.tests", "testing", "Automated tests", "high", "Add a test suite.", lambda r: exists(r, *TEST_DIRS)),
        Rule("delivery.ci", "delivery", "Continuous integration", "high", "Add a CI workflow.", has_workflow),
        Rule("project.metadata", "project", "Project metadata", "medium", "Add standard project metadata.", lambda r: exists(r, *PROJECT_FILES)),
        Rule("dependencies.lock", "reliability", "Dependency lock", "medium", "Pin dependencies with a lockfile where the ecosystem supports it.", lambda r: exists(r, *LOCK_FILES)),
        Rule("engineering.source", "engineering", "Source tree", "medium", "Include identifiable application/library source code.", has_source),
        Rule("documentation.security", "security", "Security policy", "medium", "Add SECURITY.md with responsible disclosure guidance.", lambda r: nonempty_file(r, "SECURITY.md")),
        Rule("community.contributing", "community", "Contribution guide", "low", "Add CONTRIBUTING.md to make contributions easier.", lambda r: nonempty_file(r, "CONTRIBUTING.md")),
        Rule("project.changelog", "release", "Changelog", "low", "Track user-visible changes in a changelog.", lambda r: exists(r, "CHANGELOG.md", "HISTORY.md", "CHANGES.md")),
    )


def run_checks(root: Path) -> list[Check]:
    checks: list[Check] = []
    for rule in build_rules():
        passed = bool(rule.predicate(root))
        checks.append(Check(rule.id, rule.category, rule.name, passed, rule.severity, "Present" if passed else rule.detail))
    return checks


def score(checks: list[Check]) -> int:
    weights = {"high": 3, "medium": 2, "low": 1}
    total = sum(weights[c.severity] for c in checks)
    earned = sum(weights[c.severity] for c in checks if c.passed)
    return round(100 * earned / total) if total else 0


def result(root: Path) -> dict:
    checks = run_checks(root)
    by_category: dict[str, dict[str, int]] = {}
    for check in checks:
        bucket = by_category.setdefault(check.category, {"passed": 0, "total": 0})
        bucket["total"] += 1
        bucket["passed"] += int(check.passed)
    return {
        "version": VERSION,
        "path": str(root.resolve()),
        "score": score(checks),
        "summary": {"passed": sum(c.passed for c in checks), "failed": sum(not c.passed for c in checks), "total": len(checks)},
        "categories": by_category,
        "checks": [asdict(c) for c in checks],
    }


def sarif(data: dict) -> dict:
    rules = []
    results = []
    for check in data["checks"]:
        rules.append({"id": check["id"], "shortDescription": {"text": check["name"]}, "help": {"text": check["detail"]}})
        if not check["passed"]:
            results.append({"ruleId": check["id"], "level": "warning" if check["severity"] != "high" else "error", "message": {"text": check["detail"]}})
    return {"version": "2.1.0", "$schema": "https://json.schemastore.org/sarif-2.1.0.json", "runs": [{"tool": {"driver": {"name": "RepoLens", "version": VERSION, "rules": rules}}, "results": results}]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure practical repository engineering health.")
    parser.add_argument("path", nargs="?", default=".", help="Repository path to inspect")
    parser.add_argument("--format", choices=("text", "json", "sarif"), default="text", help="Report format")
    parser.add_argument("--json", action="store_true", help="Compatibility alias for --format json")
    parser.add_argument("--min-score", type=int, metavar="N", help="Exit 2 when the score is below N")
    args = parser.parse_args()

    root = Path(args.path).expanduser()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    if args.min_score is not None and not 0 <= args.min_score <= 100:
        parser.error("--min-score must be between 0 and 100")

    data = result(root)
    output_format = "json" if args.json else args.format
    if output_format == "json":
        print(json.dumps(data, indent=2))
    elif output_format == "sarif":
        print(json.dumps(sarif(data), indent=2))
    else:
        print(f"RepoLens {data['version']} — score {data['score']}/100")
        for check in data["checks"]:
            marker = "PASS" if check["passed"] else "FAIL"
            print(f"[{marker}] {check['severity'].upper():6} {check['category']:<14} {check['name']}: {check['detail']}")

    return 2 if args.min_score is not None and data["score"] < args.min_score else 0


if __name__ == "__main__":
    raise SystemExit(main())

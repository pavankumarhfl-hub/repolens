from pathlib import Path

from repolens import run_checks, score


def test_detects_repository_hygiene(tmp_path: Path):
    for name in ("README.md", "LICENSE", ".gitignore", ".env.example"):
        (tmp_path / name).write_text("x", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / ".github" / "workflows").mkdir(parents=True)

    checks = run_checks(tmp_path)

    assert all(check.passed for check in checks)
    assert score(checks) == 100


def test_reports_missing_items(tmp_path: Path):
    checks = run_checks(tmp_path)

    assert score(checks) == 0
    assert not any(check.passed for check in checks)

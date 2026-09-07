from pathlib import Path

from repolens import result, run_checks, score


def test_full_hygiene_scores_100(tmp_path: Path):
    for name in ("README.md", "LICENSE", ".gitignore", ".env.example"):
        (tmp_path / name).write_text("x", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / ".github" / "workflows").mkdir(parents=True)

    checks = run_checks(tmp_path)

    assert all(check.passed for check in checks)
    assert score(checks) == 100


def test_empty_repository_scores_zero(tmp_path: Path):
    checks = run_checks(tmp_path)
    assert score(checks) == 0


def test_result_is_machine_readable(tmp_path: Path):
    data = result(tmp_path)
    assert data["version"] == "0.2.0"
    assert data["summary"]["total"] == 6
    assert len(data["checks"]) == 6

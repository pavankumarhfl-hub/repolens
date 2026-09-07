from pathlib import Path

from repolens import result, run_checks, sarif, score


def make_healthy_repo(root: Path) -> None:
    for name in ("README.md", "LICENSE", ".gitignore", ".env.example", "SECURITY.md", "CONTRIBUTING.md", "CHANGELOG.md", "pyproject.toml", "poetry.lock"):
        (root / name).write_text("x", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests" / "test_example.py").write_text("def test_ok(): pass", encoding="utf-8")
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("print('ok')", encoding="utf-8")
    (root / ".github" / "workflows").mkdir(parents=True)
    (root / ".github" / "workflows" / "ci.yml").write_text("name: CI", encoding="utf-8")


def test_healthy_repository_scores_100(tmp_path: Path):
    make_healthy_repo(tmp_path)
    checks = run_checks(tmp_path)
    assert all(check.passed or not check.applicable for check in checks)
    assert score(checks) == 100


def test_empty_repository_scores_zero(tmp_path: Path):
    checks = run_checks(tmp_path)
    assert score(checks) == 0
    assert len(checks) == 12
    assert sum(not check.applicable for check in checks) == 1


def test_result_contains_categories_and_summary(tmp_path: Path):
    data = result(tmp_path)
    assert data["version"] == "0.4.1"
    assert data["summary"]["total"] == 12
    assert data["summary"]["failed"] == 11
    assert data["summary"]["not_applicable"] == 1
    assert "security" in data["categories"]


def test_sarif_reports_only_applicable_failures(tmp_path: Path):
    data = result(tmp_path)
    report = sarif(data)
    assert report["version"] == "2.1.0"
    assert report["runs"][0]["tool"]["driver"]["name"] == "RepoLens"
    assert len(report["runs"][0]["results"]) == 11


def test_project_metadata_is_ecosystem_aware(tmp_path: Path):
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    checks = {check.id: check for check in run_checks(tmp_path)}
    assert checks["project.metadata"].passed
    assert not checks["dependencies.lock"].passed
    assert checks["dependencies.lock"].applicable


def test_python_project_does_not_require_optional_lockfile(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'", encoding="utf-8")
    checks = {check.id: check for check in run_checks(tmp_path)}
    assert not checks["dependencies.lock"].applicable

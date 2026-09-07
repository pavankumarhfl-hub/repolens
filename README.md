# RepoLens 🔎

**Repository engineering health intelligence for developers, teams, and CI.**

RepoLens turns a repository into a transparent engineering-health report. It evaluates maintainability signals across documentation, testing, delivery, security, project structure, dependencies, and release hygiene — without modifying the target repository.

> **Build it. Inspect it. Improve it.**

## Why RepoLens?

A repository can compile and still be difficult to maintain. Missing tests, weak documentation, absent CI, unmanaged dependencies, or no security policy create engineering risk long before production.

RepoLens provides a fast baseline that is:

- ⚡ **Lightweight** — Python standard library at runtime
- 🔍 **Transparent** — every rule has an ID, category, severity, and explanation
- 🤖 **Automation-ready** — JSON and SARIF output
- 🚦 **CI-friendly** — configurable minimum score gate
- 🌍 **Ecosystem-aware** — recognizes common project and dependency files across languages
- 🛡️ **Non-destructive** — reads repository structure; does not edit it

## What it checks

| Area | Signals |
|---|---|
| Documentation | README, security policy |
| Legal | Open-source license |
| Quality | `.gitignore` |
| Security | Environment template, security policy |
| Testing | Test directories |
| Delivery | GitHub Actions workflows |
| Project | Common ecosystem metadata |
| Reliability | Dependency lockfiles |
| Engineering | Source tree |
| Community | Contribution guide |
| Release | Changelog |

Checks are weighted by severity: **high = 3, medium = 2, low = 1**.

## Quick start

Run directly:

```bash
python src/repolens.py /path/to/repository
```

JSON for automation:

```bash
python src/repolens.py /path/to/repository --format json
```

SARIF for security/code-scanning workflows:

```bash
python src/repolens.py /path/to/repository --format sarif
```

Fail a CI job when engineering health drops below a threshold:

```bash
python src/repolens.py . --min-score 80
```

## Example output

```text
RepoLens 0.3.0 — score 83/100
[PASS] HIGH   testing        Automated tests: Present
[PASS] HIGH   delivery       Continuous integration: Present
[FAIL] MEDIUM documentation  README: Add a clear README.
```

## Design principles

1. **Useful over noisy** — checks should lead to actionable improvements.
2. **Explainable scoring** — no hidden “AI score”.
3. **Safe by default** — inspection is read-only.
4. **Composable output** — humans can read it; CI can consume it.
5. **Language-agnostic foundation** — common repository conventions first.

## Roadmap

### v0.3 — Engineering health engine
- [x] Weighted rules
- [x] Category-level reporting
- [x] JSON output
- [x] Minimum-score CI gate
- [x] SARIF output
- [x] Ecosystem-aware project/lockfile detection

### v0.4 — Deeper repository intelligence
- [ ] Configurable rule packs
- [ ] File-quality and documentation-depth signals
- [ ] Dependency freshness signals
- [ ] Git history/activity signals
- [ ] Baseline and trend comparison
- [ ] Better false-positive controls

### v0.5 — Developer workflow
- [ ] First-class GitHub Action
- [ ] PR annotations
- [ ] Score badge
- [ ] `repolens init` configuration
- [ ] Release automation

### Future
- Repository health dashboards
- Organization-wide reporting
- Historical engineering-health trends
- Plugin/rule ecosystem

## Development

```bash
python -m pip install pytest
python -m pytest -q
```

The project intentionally keeps runtime dependencies at zero.

## Contributing

Contributions are welcome. New rules should be deterministic, explainable, tested, and useful to real developers. See `CONTRIBUTING.md`.

## Security

RepoLens is designed as a read-only inspection tool. Please report security issues privately according to `SECURITY.md`.

## License

MIT

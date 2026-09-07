# RepoLens 🔎

**Repository engineering health intelligence for developers, teams, and CI.**

RepoLens turns a repository into a transparent engineering-health report. It evaluates maintainability signals across documentation, testing, delivery, security, project structure, dependencies, and release hygiene — without modifying the target repository.

[![CI](https://github.com/pavankumarhfl-hub/repolens/actions/workflows/ci.yml/badge.svg)](https://github.com/pavankumarhfl-hub/repolens/actions/workflows/ci.yml)

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

### Run from source

```bash
python src/repolens.py /path/to/repository
```

### Install locally

```bash
python -m pip install .
repolens /path/to/repository
```

JSON for automation:

```bash
repolens /path/to/repository --format json
```

SARIF for code-scanning integrations:

```bash
repolens /path/to/repository --format sarif
```

Enforce a quality bar in CI:

```bash
repolens . --min-score 80
```

## GitHub Action

Use RepoLens directly in another repository:

```yaml
name: Repository Health

on:
  push:
  pull_request:

jobs:
  repolens:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pavankumarhfl-hub/repolens@main
        with:
          min-score: 80
```

The Action exposes the calculated score as an output and can fail the workflow when the configured threshold is not met.

## Example output

```text
RepoLens 0.3.0 — score 83/100
[PASS] HIGH   testing        Automated tests: Present
[PASS] HIGH   delivery       Continuous integration: Present
[FAIL] MEDIUM documentation  README: Add a clear README.
```

## Architecture

```text
Target repository
       │
       ▼
   Rule engine
       │
       ├── Documentation
       ├── Security
       ├── Testing
       ├── Delivery
       ├── Reliability
       └── Engineering
       │
       ▼
 Weighted score
       │
       ├── Terminal
       ├── JSON
       └── SARIF
```

The rule reference is documented in `docs/rules.md`.

## Design principles

1. **Useful over noisy** — checks should lead to actionable improvements.
2. **Explainable scoring** — no hidden “AI score”.
3. **Safe by default** — inspection is read-only.
4. **Composable output** — humans can read it; CI can consume it.
5. **Language-agnostic foundation** — common repository conventions first.

## Scope and limitations

RepoLens 0.3 is intentionally a **structural engineering-health baseline**. It does not claim to understand every line of code, prove security, or replace code review, dependency scanners, test coverage tools, or static analysis. A passing score means the repository satisfies the configured structural signals — not that the software is production-safe.

The roadmap expands these signals carefully rather than hiding complexity behind an opaque score.

## Roadmap

### v0.3 — Engineering health engine
- [x] Weighted rules
- [x] Category-level reporting
- [x] JSON output
- [x] Minimum-score CI gate
- [x] SARIF output
- [x] Ecosystem-aware project/lockfile detection
- [x] Reusable GitHub Action

### v0.4 — Deeper repository intelligence
- [ ] Configurable rule packs
- [ ] File-quality and documentation-depth signals
- [ ] Dependency freshness signals
- [ ] Git history/activity signals
- [ ] Baseline and trend comparison
- [ ] Better false-positive controls

### v0.5 — Developer workflow
- [ ] PR annotations
- [ ] Score badge generation
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

Runtime dependencies remain at zero.

## Contributing

Contributions are welcome. New rules should be deterministic, explainable, tested, and useful to real developers. See `CONTRIBUTING.md`.

## Security

RepoLens is designed as a read-only inspection tool. Please report security issues privately according to `SECURITY.md`.

## License

MIT

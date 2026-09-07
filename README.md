# RepoLens 🔎

**Repository engineering health intelligence for developers, teams, and CI.**

RepoLens turns a repository into a transparent engineering-health report. It evaluates maintainability signals across documentation, testing, delivery, security, project structure, dependencies, and release hygiene — without modifying the target repository.

**Maintainer:** Pavan Kumar BN

[![CI](https://github.com/pavankumarhfl-hub/repolens/actions/workflows/ci.yml/badge.svg)](https://github.com/pavankumarhfl-hub/repolens/actions/workflows/ci.yml)

> **Build it. Inspect it. Improve it.**

## Why RepoLens?

A repository can compile and still be difficult to maintain. Missing tests, weak documentation, absent CI, unmanaged dependencies, or no security policy create engineering risk long before production.

RepoLens provides a fast baseline that is lightweight, transparent, automation-ready, CI-friendly, ecosystem-aware, and non-destructive.

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

```bash
python -m pip install .
repolens /path/to/repository
repolens /path/to/repository --format json
repolens /path/to/repository --format sarif
repolens . --min-score 80
```

## GitHub Action

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

## Architecture

```text
Target repository → Rule engine → Weighted score → Text / JSON / SARIF
                         │
             documentation · security · testing
             delivery · reliability · engineering
```

## Design principles

1. Useful over noisy.
2. Explainable scoring — no hidden AI score.
3. Safe by default — read-only inspection.
4. Composable output for humans and CI.
5. Language-agnostic repository conventions first.

## Scope and limitations

RepoLens is a **structural engineering-health baseline**. It does not prove security, understand every line of code, or replace code review, dependency scanners, coverage tools, or static analysis. A passing score means the configured structural signals are present — not that the software is production-safe.

## Roadmap

### v0.3 — Engineering health engine
- [x] Weighted rules
- [x] Category reporting
- [x] JSON and SARIF
- [x] Minimum-score CI gate
- [x] Ecosystem-aware detection
- [x] Reusable GitHub Action

### v0.4 — Deeper repository intelligence
- [ ] Configurable rule packs
- [ ] Documentation-depth signals
- [ ] Dependency freshness signals
- [ ] Git history/activity signals
- [ ] Baseline and trend comparison
- [ ] Better false-positive controls

### v0.5 — Developer workflow
- [ ] PR annotations
- [ ] Score badge generation
- [ ] `repolens init` configuration
- [ ] Release automation

## Development

```bash
python -m pip install pytest
python -m pytest -q
```

Runtime dependencies remain at zero.

## Contributing

New rules should be deterministic, explainable, tested, and useful to real developers. See `CONTRIBUTING.md`.

## Security

RepoLens is a read-only inspection tool. See `SECURITY.md` for reporting guidance.

## License

MIT — Copyright (c) 2026 Pavan Kumar BN

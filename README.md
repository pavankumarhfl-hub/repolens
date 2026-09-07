# RepoLens

**Repository engineering-hygiene scanner for developers and teams.**

RepoLens checks a repository for practical engineering signals such as documentation, licensing, tests, environment templates, and CI configuration. It produces a simple score and can emit JSON for automation.

## Why RepoLens?

A repository can contain working code and still be difficult to maintain, onboard, review, or ship. RepoLens provides a lightweight baseline check before a project is published or handed to another developer.

## Features

- Checks for README, license, `.gitignore`, and `.env.example`
- Checks for tests and GitHub Actions workflow configuration
- Human-readable terminal output
- JSON output for scripts and CI
- Zero runtime dependencies
- Non-destructive: it only inspects the target directory

## Quick start

```bash
python src/repolens.py /path/to/repository
python src/repolens.py /path/to/repository --json
```

## Development

```bash
python -m pip install pytest
python -m pytest -q
```

## Status

**v0.1.0 — working foundation.**

The current scoring model is intentionally small and transparent. Future releases can add configurable checks, severity levels, richer reports, and additional CI/platform signals without turning RepoLens into a heavyweight dependency.

## License

MIT

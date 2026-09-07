# Contributing to RepoLens

Thanks for contributing to RepoLens.

**Maintainer:** Pavan Kumar BN

## Before opening a change

- Explain the problem the rule or feature solves.
- Keep runtime dependencies at zero unless there is a strong reason otherwise.
- Add tests for new behavior and edge cases.
- Keep rules deterministic and explainable.
- Avoid collecting or printing secret values.

## New rules

A rule should have:

- a stable rule ID
- a category
- a severity
- an actionable failure message
- automated tests

Prefer repository conventions that work across ecosystems instead of assumptions tied to one language.

## Pull requests

Keep pull requests focused. Describe the behavior change, testing performed, and any compatibility impact.

## Attribution

Project maintainer and original author: **Pavan Kumar BN**.

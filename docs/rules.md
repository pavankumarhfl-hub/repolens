# RepoLens rule reference

RepoLens currently ships with 12 deterministic baseline rules.

| Rule | Category | Severity | What it means |
|---|---|---|---|
| `documentation.readme` | documentation | medium | A non-empty README exists. |
| `legal.license` | legal | high | A recognized license file exists. |
| `quality.gitignore` | quality | medium | A non-empty `.gitignore` exists. |
| `security.env-template` | security | high | A safe environment template exists. |
| `testing.tests` | testing | high | A conventional test directory exists. |
| `delivery.ci` | delivery | high | At least one GitHub Actions workflow exists. |
| `project.metadata` | project | medium | Common ecosystem project metadata exists. |
| `dependencies.lock` | reliability | medium | A recognized dependency lockfile exists. |
| `engineering.source` | engineering | medium | A source directory or recognizable source file exists. |
| `documentation.security` | security | medium | `SECURITY.md` exists and is non-empty. |
| `community.contributing` | community | low | `CONTRIBUTING.md` exists and is non-empty. |
| `project.changelog` | release | low | A changelog file exists. |

## Scoring

Each rule contributes according to severity:

- High: 3 points
- Medium: 2 points
- Low: 1 point

The score is the percentage of available weighted points that passed, rounded to the nearest integer.

The rule engine intentionally favors explainability over opaque heuristics. More advanced signals can be introduced as separate, documented rules in future releases.

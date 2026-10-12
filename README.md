# template-python

A GitHub template for a new murphy360 Python project. It starts with CI, lint, the ratchet, Dependabot, the
`CLAUDE.md`, a Dockerfile, the issue and pull request templates and the milestone conventions already in place,
all from [murphy360/standards](https://github.com/murphy360/standards).

## Start a project

```bash
gh repo create <name> --template murphy360/template-python --private --clone
```

CI is green on the first push, untouched. Then make it yours. These are the lines to change:

| File | What to change |
|---|---|
| `pyproject.toml` | `name`, `description`; add your dependencies |
| `src/my_service/` | rename the directory to your package name, and fix `tests/test_smoke.py` to import it |
| `.github/workflows/ci.yml` | `image: my-service` to your image name, and `push: false` to `push: ${{ github.event_name != 'pull_request' }}` (the template only builds, so it never publishes) |
| `CLAUDE.md` | fill in "This project" at the end |
| `Dockerfile` | the `CMD`, once the project has a service to run |
| `README.md` | replace this file with your own |
| `docs/MILESTONES.md` | keep it, or change it where you work differently, and say why |

Keep the jobs in `ci.yml` that apply. Delete the ones that do not (for example `shell` when there are no `.sh` files).

## Build and test

Tests run in Docker, not on the host. Use your own tag for the image.

```bash
docker build -t my-service:test .
docker run --rm my-service:test                          # runs pytest -q
docker run --rm -v "$PWD:/src" -w /src my-service:test pytest -q   # the same, on your working tree
```

The code rules, as CI runs them (ruff 0.6.9, a copy of murphy360/standards next to the project):

```bash
pip install ruff==0.6.9
python3 <standards>/tools/code_rules.py --all   # every file: ruff, no noqa, complexity, file size, format
python3 <standards>/tools/check_standards.py
```

Every file is clean, and CI checks every file on every run. There is no baseline: a finding anywhere fails.

## Take standards updates

CI calls the shared workflows at a version tag, `murphy360/standards/...@v2`. A compatible change moves the `v2`
tag, so you get it with no edit. To move to a new major version, change every `@v2` in `.github/workflows/ci.yml`
to the new tag (for example `@v3`) and read the standards' release notes for what else to change. The templates
(`CLAUDE.md`, `dependabot.yml`, `ci.yml`) are copies: when the standards change them, compare and take what you want.

## What is here

| Path | What it is |
|---|---|
| `.github/workflows/ci.yml` | CI: standards check, lint, shell lint, workflow lint, tests, image |
| `.github/dependabot.yml` | weekly grouped updates for actions, pip and docker |
| `.github/ISSUE_TEMPLATE/ticket.md` | the ticket shape: Problem, What to build, For the implementer, Done |
| `.github/pull_request_template.md` | the PR body: what and why, `Closes #N`, tests, docs, known issues |
| `CLAUDE.md` | how an agent session works in the project |
| `docs/MILESTONES.md` | the milestone conventions |
| `pyproject.toml`, `src/`, `tests/`, `Dockerfile` | a package with one passing test, and the image that runs it |

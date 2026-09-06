# Contributing

Thank you for contributing to the AI Service Desk Agent project.

This document explains how to set up a development environment and how to remove the checked-in virtual environment (.venv) from the repository if it exists.

## Development environment

1. Create a Python virtual environment (do not commit it to the repo):

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\Activate.ps1 # Windows PowerShell
```

2. Install pinned dependencies (see requirements.txt):

```bash
pip install -r requirements.txt
```

3. Create a local `.env` file with ServiceNow credentials (example):

```env
SERVICENOW_INSTANCE=https://your-instance.service-now.com
SERVICENOW_USERNAME=admin
SERVICENOW_PASSWORD=your-password
```

> Never commit `.env` to the repository. `.env` is already ignored by `.gitignore`.

## Removing a checked-in .venv directory (if present)

If a `.venv` directory was accidentally committed, remove it from git history in three steps:

1. Remove the files from the index while keeping them locally:

```bash
git rm -r --cached .venv
git commit -m "chore: remove checked-in virtualenv (.venv)"
git push origin faang/initial-hardening
```

2. Confirm `.venv/` is present in `.gitignore` (it is by default). This prevents re-adding it.

3. Optionally remove the files from the repository history entirely (only if necessary and you understand the implications):

```bash
# Use with caution — rewrites history
bfg --delete-folders .venv
git push --force
```

## Development workflow

- Use the `faang/*` branch namespace for hardening and feature branches targeting FAANG readiness.
- Run linters and tests before opening a PR.

## Contact

If you are unsure about any step, open an issue or a draft PR and tag @Madhuchandana-ux.

# env-guard-cli

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://github.com/jishanahmed-shaikh/env-guard-cli/actions/workflows/ci.yml/badge.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

**Catch exposed `.env` files before they reach GitHub.**

`env-guard-cli` recursively scans your project for `.env` files that aren't covered by any `.gitignore` — a simple security check that takes seconds and can save you from a very bad day.

---

## The Problem

You create `.env.local`, `.env.staging`, or `.env.test` during development and forget to add them to `.gitignore`. One `git push` later, your API keys are public. This tool exists to prevent exactly that.

---

## Install

```bash
pip install env-guard-cli
```

From source:

```bash
git clone https://github.com/jishanahmed-shaikh/env-guard-cli.git
cd env-guard-cli
pip install -e .
```

---

## Usage

```bash
# Scan current directory
env-guard

# Scan a specific path
env-guard /path/to/project

# Fail with exit code 1 if any exposed files found (CI-friendly)
env-guard --strict

# Show version
env-guard --version
```

### Output

```
🔍 Scanning: /home/user/myproject

✅ Protected (1):
   /home/user/myproject/.env

⚠️  EXPOSED (1) — not in any .gitignore:
   /home/user/myproject/.env.local

  Add these to your .gitignore to prevent accidental commits.
```

---

## CI Integration

Drop this into any GitHub Actions workflow to block pushes with exposed secrets:

```yaml
- name: Check for exposed .env files
  run: env-guard --strict
```

Exit code `0` = all clear. Exit code `1` = exposed files found (only with `--strict`).

---

## How It Works

1. Walks the target directory recursively, skipping `.git`, `node_modules`, `.venv`, `__pycache__`
2. Collects all `.env` and `.env.*` files
3. For each file, walks up the directory tree looking for a `.gitignore`
4. Checks if the file matches any pattern in that `.gitignore`
5. Reports what's protected and what's exposed

Patterns supported: exact names (`.env`), prefix wildcards (`.env*`), suffix wildcards (`*.env`), and relative paths.

---

## What Gets Scanned

| File | Detected |
|------|----------|
| `.env` | ✅ |
| `.env.local` | ✅ |
| `.env.staging` | ✅ |
| `.env.test` | ✅ |
| `config.py` | ❌ (not a .env file) |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports and PRs are welcome.

## License

[MIT](LICENSE) — © 2026 Jishanahmed AR Shaikh

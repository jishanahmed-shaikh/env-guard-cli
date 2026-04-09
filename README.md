# env-guard-cli

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat)
![CLI](https://img.shields.io/badge/Tool-CLI-orange?style=flat)
![Security](https://img.shields.io/badge/Focus-Security-red?style=flat)

Catch exposed `.env` files before they reach GitHub.

---

## The Problem

You create `.env.local`, `.env.staging`, or `.env.test` during development and forget to add them to `.gitignore`. One `git push` later, your API keys are public. This tool exists to prevent exactly that.

It scans your project recursively, checks every `.env` file against the nearest `.gitignore`, and tells you exactly what is protected and what is not.

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

### Sample Output

```
🔍 Scanning: /home/user/myproject

✅ Protected (1):
   /home/user/myproject/.env

⚠️  EXPOSED (1) — not in any .gitignore:
   /home/user/myproject/.env.local

  Add these to your .gitignore to prevent accidental commits.
```

---

## Drop it into CI

```yaml
- name: Check for exposed .env files
  run: env-guard --strict
```

Exit code `0` means all clear. Exit code `1` means something is exposed (only triggered with `--strict`).

---

## How It Works

The scanner walks your directory tree and for each `.env` file found, it climbs up the folder hierarchy looking for a `.gitignore`. It then checks whether the file matches any pattern in that file.

Supported pattern types:

- Exact match: `.env`
- Prefix wildcard: `.env*`
- Suffix wildcard: `*.env`
- Relative path: `config/.env`

Skipped directories: `.git`, `node_modules`, `.venv`, `__pycache__`

---

## What Gets Detected

| File | Scanned |
|------|---------|
| `.env` | yes |
| `.env.local` | yes |
| `.env.staging` | yes |
| `.env.test` | yes |
| `config.py` | no |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports and PRs are welcome.

## License

[MIT](LICENSE) © 2026 Jishanahmed AR Shaikh

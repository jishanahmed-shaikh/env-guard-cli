# env-guard-cli

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://github.com/jishanahmed-shaikh/env-guard-cli/actions/workflows/ci.yml/badge.svg)

> Scan your project directories for `.env` files that are accidentally **not** covered by `.gitignore` — before you push secrets to GitHub.

---

## Why

It's easy to create a `.env.local` or `.env.staging` and forget to add it to `.gitignore`. This tool catches that before it becomes a breach.

---

## Install

```bash
pip install env-guard-cli
```

Or run directly from source:

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

# Exit with code 1 if any exposed files found (great for CI)
env-guard --strict
```

### Example Output

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

Add to your GitHub Actions workflow:

```yaml
- name: Check for exposed .env files
  run: env-guard --strict
```

---

## How It Works

1. Recursively walks the target directory (skips `.git`, `node_modules`, `.venv`)
2. Finds all `.env` and `.env.*` files
3. Walks up the directory tree from each file looking for a `.gitignore`
4. Checks if the file is covered by any pattern in that `.gitignore`
5. Reports protected vs. exposed files

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)

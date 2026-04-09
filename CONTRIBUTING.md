# Contributing to env-guard-cli

Thanks for taking the time to contribute! Here's how to get started.

## Setup

```bash
git clone https://github.com/jishanahmed-shaikh/env-guard-cli.git
cd env-guard-cli
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Guidelines

- Keep PRs focused — one feature or fix per PR
- Add tests for any new logic
- Follow existing code style (PEP 8)
- Update `README.md` if behavior changes

## Reporting Issues

Open an issue at [GitHub Issues](https://github.com/jishanahmed-shaikh/env-guard-cli/issues) with:
- What you expected
- What actually happened
- Steps to reproduce

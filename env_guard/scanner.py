"""Core scanner logic for detecting unprotected .env files."""

import os
from pathlib import Path
from typing import List, Tuple


def find_env_files(root: Path) -> List[Path]:
    """Recursively find all .env* files under root, skipping hidden dirs."""
    env_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden directories like .git, .venv, node_modules
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".") and d not in ("node_modules", "__pycache__", ".venv", "venv")
        ]
        for filename in filenames:
            if filename == ".env" or filename.startswith(".env."):
                env_files.append(Path(dirpath) / filename)
    return env_files


def load_gitignore_patterns(gitignore_path: Path) -> List[str]:
    """Load patterns from a .gitignore file."""
    if not gitignore_path.exists():
        return []
    lines = gitignore_path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def is_ignored(env_file: Path, gitignore_dir: Path, patterns: List[str]) -> bool:
    """Check if an env file is covered by any gitignore pattern."""
    relative = env_file.relative_to(gitignore_dir)
    name = env_file.name

    for pattern in patterns:
        # Direct filename match
        if pattern == name:
            return True
        # Pattern like .env* or *.env
        if pattern.endswith("*") and name.startswith(pattern[:-1]):
            return True
        if pattern.startswith("*") and name.endswith(pattern[1:]):
            return True
        # Relative path match
        if pattern.lstrip("/") == str(relative).replace("\\", "/"):
            return True
        # Wildcard glob-style: **.env
        if pattern.replace("**", "").strip("/") == name:
            return True

    return False


def scan(root: str) -> Tuple[List[Path], List[Path]]:
    """
    Scan a directory tree for .env files and check gitignore coverage.

    Returns:
        (safe, exposed): lists of protected and unprotected .env paths
    """
    root_path = Path(root).resolve()
    env_files = find_env_files(root_path)

    safe: List[Path] = []
    exposed: List[Path] = []

    for env_file in env_files:
        # Walk up from env_file's dir to root looking for .gitignore
        covered = False
        check_dir = env_file.parent
        while True:
            gitignore = check_dir / ".gitignore"
            patterns = load_gitignore_patterns(gitignore)
            if patterns and is_ignored(env_file, check_dir, patterns):
                covered = True
                break
            if check_dir == root_path or check_dir.parent == check_dir:
                break
            check_dir = check_dir.parent

        if covered:
            safe.append(env_file)
        else:
            exposed.append(env_file)

    return safe, exposed

"""Tests for env_guard.scanner."""

import pytest
from pathlib import Path
from env_guard.scanner import find_env_files, is_ignored, load_gitignore_patterns, scan


def test_find_env_files(tmp_path):
    (tmp_path / ".env").write_text("SECRET=1")
    (tmp_path / ".env.local").write_text("LOCAL=1")
    (tmp_path / "config.py").write_text("x = 1")

    found = find_env_files(tmp_path)
    names = [f.name for f in found]
    assert ".env" in names
    assert ".env.local" in names
    assert "config.py" not in names


def test_load_gitignore_patterns(tmp_path):
    gi = tmp_path / ".gitignore"
    gi.write_text("# comment\n.env\n*.log\n\n")
    patterns = load_gitignore_patterns(gi)
    assert ".env" in patterns
    assert "*.log" in patterns
    assert "# comment" not in patterns


def test_load_gitignore_missing(tmp_path):
    patterns = load_gitignore_patterns(tmp_path / ".gitignore")
    assert patterns == []


def test_is_ignored_direct_match(tmp_path):
    env = tmp_path / ".env"
    env.write_text("")
    assert is_ignored(env, tmp_path, [".env"]) is True


def test_is_ignored_wildcard(tmp_path):
    env = tmp_path / ".env.local"
    env.write_text("")
    assert is_ignored(env, tmp_path, [".env*"]) is True


def test_is_ignored_no_match(tmp_path):
    env = tmp_path / ".env"
    env.write_text("")
    assert is_ignored(env, tmp_path, ["*.log", "node_modules"]) is False


def test_scan_exposed(tmp_path):
    (tmp_path / ".env").write_text("SECRET=1")
    safe, exposed = scan(str(tmp_path))
    assert len(exposed) == 1
    assert len(safe) == 0


def test_scan_protected(tmp_path):
    (tmp_path / ".env").write_text("SECRET=1")
    (tmp_path / ".gitignore").write_text(".env\n")
    safe, exposed = scan(str(tmp_path))
    assert len(safe) == 1
    assert len(exposed) == 0


def test_scan_nested(tmp_path):
    sub = tmp_path / "subproject"
    sub.mkdir()
    (sub / ".env").write_text("SECRET=1")
    (tmp_path / ".gitignore").write_text(".env\n")
    safe, exposed = scan(str(tmp_path))
    assert len(safe) == 1
    assert len(exposed) == 0

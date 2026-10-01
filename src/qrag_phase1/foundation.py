"""Foundation helpers for QRAG Phase 1."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Iterable


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Return the SHA-256 digest of a file."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)

    return digest.hexdigest()


def run_git_command(project_root: Path, *args: str) -> str:
    """Run one read-only Git command inside the project repository."""
    result = subprocess.run(
        ["git", "-C", str(project_root), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def collect_git_info(project_root: Path) -> dict[str, Any]:
    """Collect the Git branch, commit and working-tree state."""
    branch = run_git_command(project_root, "branch", "--show-current")
    commit_sha = run_git_command(project_root, "rev-parse", "HEAD")
    commit_short = run_git_command(
        project_root,
        "rev-parse",
        "--short",
        "HEAD",
    )
    last_commit = run_git_command(
        project_root,
        "log",
        "-1",
        "--pretty=format:%h | %ad | %s",
        "--date=iso-strict",
    )
    status = run_git_command(project_root, "status", "--porcelain")

    return {
        "branch": branch,
        "commit_sha": commit_sha,
        "commit_short": commit_short,
        "last_commit": last_commit,
        "working_tree": "clean" if not status else "dirty",
        "porcelain_status": status.splitlines() if status else [],
    }


def collect_repository_inventory(
    project_root: Path,
    required_paths: Iterable[str],
    key_files: Iterable[str],
) -> dict[str, Any]:
    """Collect a lightweight repository inventory."""
    required_path_status = {}

    for relative_path in required_paths:
        path = project_root / relative_path
        required_path_status[relative_path] = path.exists()

    key_file_status = {}

    for relative_path in key_files:
        path = project_root / relative_path
        entry = {
            "exists": path.is_file(),
        }

        if path.is_file():
            entry["size_bytes"] = path.stat().st_size

        key_file_status[relative_path] = entry

    return {
        "required_paths": required_path_status,
        "required_paths_ok": all(required_path_status.values()),
        "key_files": key_file_status,
    }


def write_json_atomic(
    path: Path,
    payload: Any,
    *,
    ensure_ascii: bool = False,
    indent: int = 2,
) -> None:
    """Write JSON atomically using a temporary file in the target directory."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        json.dump(
            payload,
            handle,
            ensure_ascii=ensure_ascii,
            indent=indent,
            sort_keys=True,
        )
        handle.write("\n")
        temporary_path = Path(handle.name)

    temporary_path.replace(path)

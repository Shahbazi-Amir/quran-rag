"""Tests for QRAG Phase 1 foundation helpers."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from qrag_phase1.foundation import (
    collect_git_info,
    collect_repository_inventory,
    sha256_file,
    write_json_atomic,
)


class FoundationTests(unittest.TestCase):
    def test_sha256_file_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("QRAG\n", encoding="utf-8")

            first = sha256_file(path)
            second = sha256_file(path)

            self.assertEqual(first, second)
            self.assertEqual(len(first), 64)

    def test_write_json_atomic_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            payload = {"status": "PASS", "count": 3}

            write_json_atomic(path, payload)

            reloaded = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(reloaded, payload)

    def test_repository_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git").mkdir()
            (root / "notebooks").mkdir()
            (root / "data").mkdir()
            (root / "key.txt").write_text("x", encoding="utf-8")

            result = collect_repository_inventory(
                project_root=root,
                required_paths=[".git", "notebooks", "data"],
                key_files=["key.txt", "missing.txt"],
            )

            self.assertTrue(result["required_paths_ok"])
            self.assertTrue(result["key_files"]["key.txt"]["exists"])
            self.assertFalse(result["key_files"]["missing.txt"]["exists"])

    def test_collect_git_info(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            subprocess.run(
                ["git", "init", "-b", "qrag-phase1", str(root)],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                ["git", "-C", str(root), "config", "user.name", "QRAG Test"],
                check=True,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "config",
                    "user.email",
                    "qrag@example.test",
                ],
                check=True,
            )

            sample = root / "sample.txt"
            sample.write_text("baseline\n", encoding="utf-8")

            subprocess.run(
                ["git", "-C", str(root), "add", "sample.txt"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(root), "commit", "-m", "baseline"],
                check=True,
                capture_output=True,
                text=True,
            )

            result = collect_git_info(root)

            self.assertEqual(result["branch"], "qrag-phase1")
            self.assertEqual(result["working_tree"], "clean")
            self.assertEqual(len(result["commit_sha"]), 40)


if __name__ == "__main__":
    unittest.main()

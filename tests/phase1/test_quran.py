"""Tests for QRAG canonical Quran helpers."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from qrag_phase1.quran import (
    build_canonical_quran_records,
    parse_quran_pipe_file,
    read_jsonl,
    sha256_file,
    validate_quran_records,
    write_jsonl_atomic,
)


class QuranFoundationTests(unittest.TestCase):
    def _make_synthetic_quran(self, root: Path) -> Path:
        path = root / "quran.txt"
        lines = ["# synthetic header"]
        for surah in range(1, 115):
            lines.append(f"{surah}|1|text-{surah}")
        path.write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )
        return path

    def test_parse_and_validate_complete_synthetic_quran(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = self._make_synthetic_quran(Path(directory))
            parsed = parse_quran_pipe_file(path)
            result = validate_quran_records(
                parsed["records"],
                [1] * 114,
            )

            self.assertEqual(result["status"], "PASS")
            self.assertEqual(parsed["duplicate_keys"], [])
            self.assertEqual(parsed["malformed_lines"], [])

    def test_duplicate_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "quran.txt"
            path.write_text(
                "1|1|a\n1|1|b\n",
                encoding="utf-8",
            )
            parsed = parse_quran_pipe_file(path)

            self.assertEqual(
                parsed["duplicate_keys"],
                ["1:1"],
            )

    def test_malformed_record_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "quran.txt"
            path.write_text(
                "not-a-valid-record\n",
                encoding="utf-8",
            )
            parsed = parse_quran_pipe_file(path)

            self.assertEqual(len(parsed["malformed_lines"]), 1)

    def test_canonical_round_trip_preserves_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._make_synthetic_quran(root)
            parsed = parse_quran_pipe_file(path)
            raw_hash = sha256_file(path)
            rows = build_canonical_quran_records(
                parsed["records"],
                "quran:test",
                raw_hash,
            )
            output = root / "canonical.jsonl"

            write_jsonl_atomic(output, rows)
            reloaded = read_jsonl(output)

            self.assertEqual(len(reloaded), 114)
            self.assertEqual(
                reloaded[0]["arabic_uthmani"],
                "text-1",
            )
            self.assertEqual(
                reloaded[-1]["arabic_uthmani"],
                "text-114",
            )
            self.assertEqual(
                reloaded[0]["raw_sha256"],
                raw_hash,
            )


if __name__ == "__main__":
    unittest.main()

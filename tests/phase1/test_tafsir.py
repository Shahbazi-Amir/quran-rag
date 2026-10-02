"""Tests for QRAG tafsir ingestion helpers."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from qrag_phase1.tafsir import (
    read_jsonl,
    validate_tafsir_rows,
    write_jsonl_atomic,
)


class TafsirTests(unittest.TestCase):
    def test_valid_row_passes(self) -> None:
        rows = [{
            "tafsir_record_id": "t:1",
            "tafsir_id": "t",
            "text": "sample",
            "source_locator": "vol1:p1",
            "surah": 1,
            "verse_start": 1,
            "verse_end": 1,
        }]

        result = validate_tafsir_rows(rows, "t")
        self.assertEqual(result["status"], "PASS")

    def test_empty_text_fails(self) -> None:
        rows = [{
            "tafsir_record_id": "t:1",
            "tafsir_id": "t",
            "text": " ",
            "source_locator": "vol1:p1",
            "surah": 1,
            "verse_start": 1,
            "verse_end": 1,
        }]

        result = validate_tafsir_rows(rows, "t")
        self.assertEqual(result["status"], "FAIL")

    def test_duplicate_record_id_fails(self) -> None:
        row = {
            "tafsir_record_id": "t:1",
            "tafsir_id": "t",
            "text": "sample",
            "source_locator": "vol1:p1",
            "surah": 1,
            "verse_start": 1,
            "verse_end": 1,
        }

        result = validate_tafsir_rows([row, dict(row)], "t")
        self.assertEqual(result["status"], "FAIL")

    def test_jsonl_round_trip(self) -> None:
        rows = [{
            "tafsir_record_id": "t:1",
            "tafsir_id": "t",
            "text": "sample",
            "source_locator": "vol1:p1",
            "surah": 1,
            "verse_start": 1,
            "verse_end": 1,
        }]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tafsir.jsonl"
            write_jsonl_atomic(path, rows)
            self.assertEqual(read_jsonl(path), rows)


if __name__ == "__main__":
    unittest.main()

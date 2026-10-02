"""Tests for QRAG translation helpers."""

from __future__ import annotations

import unittest

from qrag_phase1.translation import (
    build_translation_records,
    validate_translation_alignment,
)


class TranslationTests(unittest.TestCase):
    def test_build_and_align(self) -> None:
        quran = [
            {"surah": 1, "ayah": 1},
            {"surah": 1, "ayah": 2},
        ]
        parsed = [
            {"surah": 1, "ayah": 1, "text": "الف", "line_number": 1},
            {"surah": 1, "ayah": 2, "text": "ب", "line_number": 2},
        ]
        rows = build_translation_records(
            parsed,
            "fa.test",
            "translation:test",
            "abc",
        )
        result = validate_translation_alignment(quran, rows)
        self.assertEqual(result["status"], "PASS")

    def test_alignment_failure_is_detected(self) -> None:
        quran = [
            {"surah": 1, "ayah": 1},
            {"surah": 1, "ayah": 2},
        ]
        translation = [
            {"surah": 1, "ayah": 1, "text": "الف"},
            {"surah": 1, "ayah": 3, "text": "ب"},
        ]
        result = validate_translation_alignment(quran, translation)
        self.assertEqual(result["status"], "FAIL")

    def test_empty_translation_is_detected(self) -> None:
        quran = [{"surah": 1, "ayah": 1}]
        translation = [{"surah": 1, "ayah": 1, "text": "   "}]
        result = validate_translation_alignment(quran, translation)
        self.assertEqual(result["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()

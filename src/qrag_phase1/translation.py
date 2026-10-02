"""Translation helpers for QRAG Phase 1."""

from __future__ import annotations

from typing import Any


def build_translation_records(
    parsed_records: list[dict[str, Any]],
    translation_id: str,
    source_id: str,
    raw_sha256: str,
) -> list[dict[str, Any]]:
    """Build verse-aligned translation records without text normalization."""
    output = []
    for record in parsed_records:
        surah = int(record["surah"])
        ayah = int(record["ayah"])
        output.append({
            "translation_record_id": f"{translation_id}:{surah}:{ayah}",
            "translation_id": translation_id,
            "verse_id": f"quran:{surah}:{ayah}",
            "surah": surah,
            "ayah": ayah,
            "text": record["text"],
            "source_id": source_id,
            "raw_sha256": raw_sha256,
            "raw_line_number": int(record["line_number"]),
        })
    return output


def validate_translation_alignment(
    quran_rows: list[dict[str, Any]],
    translation_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Validate exact verse-key alignment against canonical Quran records."""
    quran_keys = [
        (int(row["surah"]), int(row["ayah"]))
        for row in quran_rows
    ]
    translation_keys = [
        (int(row["surah"]), int(row["ayah"]))
        for row in translation_rows
    ]
    empty_text = [
        f'{row["surah"]}:{row["ayah"]}'
        for row in translation_rows
        if not str(row["text"]).strip()
    ]

    checks = {
        "record_count_equal": len(quran_rows) == len(translation_rows),
        "verse_keys_exact_match": quran_keys == translation_keys,
        "empty_translation_text_zero": len(empty_text) == 0,
    }

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "quran_count": len(quran_rows),
        "translation_count": len(translation_rows),
        "empty_text": empty_text[:100],
    }

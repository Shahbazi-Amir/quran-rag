"""Tafsir ingestion helpers for QRAG Phase 1."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Iterable


REQUIRED_TAFSIR_FIELDS = {
    "tafsir_record_id",
    "tafsir_id",
    "text",
    "source_locator",
    "surah",
    "verse_start",
    "verse_end",
}


def validate_tafsir_rows(
    rows: list[dict[str, Any]],
    tafsir_id: str,
) -> dict[str, Any]:
    """Validate structured tafsir rows before corpus acceptance."""
    errors: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for row_number, row in enumerate(rows, start=1):
        missing = REQUIRED_TAFSIR_FIELDS - set(row)

        if missing:
            errors.append({
                "row": row_number,
                "reason": "MISSING_FIELDS",
                "fields": sorted(missing),
            })
            continue

        if row["tafsir_id"] != tafsir_id:
            errors.append({
                "row": row_number,
                "reason": "TAFSIR_ID_MISMATCH",
            })

        record_id = str(row["tafsir_record_id"])

        if record_id in seen_ids:
            errors.append({
                "row": row_number,
                "reason": "DUPLICATE_RECORD_ID",
            })

        seen_ids.add(record_id)

        if not str(row["text"]).strip():
            errors.append({
                "row": row_number,
                "reason": "EMPTY_TEXT",
            })

        surah = int(row["surah"])
        verse_start = int(row["verse_start"])
        verse_end = int(row["verse_end"])

        if not 1 <= surah <= 114:
            errors.append({
                "row": row_number,
                "reason": "INVALID_SURAH",
            })

        if verse_start < 1 or verse_end < verse_start:
            errors.append({
                "row": row_number,
                "reason": "INVALID_VERSE_RANGE",
            })

        if not str(row["source_locator"]).strip():
            errors.append({
                "row": row_number,
                "reason": "EMPTY_SOURCE_LOCATOR",
            })

    return {
        "status": "PASS" if not errors else "FAIL",
        "record_count": len(rows),
        "error_count": len(errors),
        "errors": errors[:200],
    }


def write_jsonl_atomic(
    path: Path,
    rows: Iterable[dict[str, Any]],
) -> None:
    """Write tafsir rows atomically as JSONL."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        for row in rows:
            handle.write(
                json.dumps(row, ensure_ascii=False, sort_keys=True)
            )
            handle.write("\n")
        temporary_path = Path(handle.name)

    temporary_path.replace(path)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read tafsir JSONL rows."""
    rows = []

    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            if raw_line.strip():
                rows.append(json.loads(raw_line))

    return rows

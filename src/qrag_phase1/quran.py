"""Canonical Quran helpers for QRAG Phase 1."""

from __future__ import annotations

import hashlib
import json
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Return a SHA-256 digest for a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def parse_quran_pipe_file(path: Path) -> dict[str, Any]:
    """Parse a pipe-delimited Quran file while preserving verse text."""
    headers: list[str] = []
    records: list[dict[str, Any]] = []
    malformed_lines: list[dict[str, Any]] = []
    seen: set[tuple[int, int]] = set()
    duplicate_keys: list[str] = []

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.rstrip("\r\n")
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith("#"):
                headers.append(stripped)
                continue

            parts = line.split("|", 2)
            if len(parts) != 3:
                malformed_lines.append({
                    "line_number": line_number,
                    "reason": "EXPECTED_THREE_PIPE_FIELDS",
                })
                continue

            surah_raw, ayah_raw, text = parts

            try:
                surah = int(surah_raw.strip())
                ayah = int(ayah_raw.strip())
            except ValueError:
                malformed_lines.append({
                    "line_number": line_number,
                    "reason": "NON_INTEGER_SURAH_OR_AYAH",
                })
                continue

            key = (surah, ayah)
            if key in seen:
                duplicate_keys.append(f"{surah}:{ayah}")
            seen.add(key)

            records.append({
                "surah": surah,
                "ayah": ayah,
                "text": text,
                "line_number": line_number,
            })

    return {
        "headers": headers,
        "records": records,
        "malformed_lines": malformed_lines,
        "duplicate_keys": duplicate_keys,
    }


def expected_verse_keys(verse_counts: Iterable[int]) -> list[tuple[int, int]]:
    """Build the canonical ordered verse-key sequence."""
    counts = list(verse_counts)
    keys: list[tuple[int, int]] = []
    for surah, count in enumerate(counts, start=1):
        keys.extend((surah, ayah) for ayah in range(1, count + 1))
    return keys


def validate_quran_records(
    records: list[dict[str, Any]],
    verse_counts: Iterable[int],
) -> dict[str, Any]:
    """Validate Quran identity, ordering, completeness and text presence."""
    counts = list(verse_counts)
    expected_keys = expected_verse_keys(counts)
    actual_keys = [(int(r["surah"]), int(r["ayah"])) for r in records]
    key_counts = Counter(actual_keys)

    empty_text = [
        f'{r["surah"]}:{r["ayah"]}'
        for r in records
        if not str(r["text"]).strip()
    ]
    duplicate_keys = sorted(
        f"{surah}:{ayah}"
        for (surah, ayah), count in key_counts.items()
        if count > 1
    )
    missing = sorted(set(expected_keys) - set(actual_keys))
    unexpected = sorted(set(actual_keys) - set(expected_keys))

    actual_per_surah = Counter(surah for surah, _ in actual_keys)
    per_surah_mismatch = {
        str(surah): {
            "expected": counts[surah - 1],
            "actual": actual_per_surah.get(surah, 0),
        }
        for surah in range(1, len(counts) + 1)
        if actual_per_surah.get(surah, 0) != counts[surah - 1]
    }

    checks = {
        "surah_count_114": len(counts) == 114,
        "record_count_matches": len(records) == sum(counts),
        "keys_exact_match": actual_keys == expected_keys,
        "duplicate_keys_zero": len(duplicate_keys) == 0,
        "missing_keys_zero": len(missing) == 0,
        "unexpected_keys_zero": len(unexpected) == 0,
        "empty_text_zero": len(empty_text) == 0,
        "per_surah_counts_match": len(per_surah_mismatch) == 0,
    }

    return {
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "expected_record_count": sum(counts),
        "actual_record_count": len(records),
        "duplicate_keys": duplicate_keys,
        "missing_keys": [f"{s}:{a}" for s, a in missing[:100]],
        "unexpected_keys": [f"{s}:{a}" for s, a in unexpected[:100]],
        "empty_text": empty_text[:100],
        "per_surah_mismatch": per_surah_mismatch,
    }


def build_canonical_quran_records(
    records: list[dict[str, Any]],
    source_id: str,
    raw_sha256: str,
) -> list[dict[str, Any]]:
    """Build canonical verse records without altering Arabic verse text."""
    output = []
    for record in records:
        surah = int(record["surah"])
        ayah = int(record["ayah"])
        output.append({
            "verse_id": f"quran:{surah}:{ayah}",
            "surah": surah,
            "ayah": ayah,
            "arabic_uthmani": record["text"],
            "source_id": source_id,
            "raw_sha256": raw_sha256,
            "raw_line_number": int(record["line_number"]),
        })
    return output


def write_jsonl_atomic(
    path: Path,
    rows: Iterable[dict[str, Any]],
) -> None:
    """Write JSONL atomically."""
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
    """Read JSONL records."""
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            if raw_line.strip():
                rows.append(json.loads(raw_line))
    return rows

# NB07 — Tafsir Ingestion and Acceptance

## Status
`PENDING_LOCAL_RUN_ALL`

## Expected current outcome
`BLOCKED` with reason `SOURCE_PACKAGE_MISSING` for tafsir sources that have not yet been acquired.

This is an expected fail-closed state, not a coding failure.

## Source package contract
Each tafsir must be delivered under:

`data/phase1/raw/tafsir/<safe-tafsir-id>/source_manifest.json`

and

`data/phase1/raw/tafsir/<safe-tafsir-id>/records.jsonl`

The source manifest must identify edition, language, rights evidence, acquisition URL/time, and raw files.

## Acceptance rule
Only a package with `rights.status=verified_allowed` and structurally valid records can be published into `data/phase1/processed/tafsir/`.

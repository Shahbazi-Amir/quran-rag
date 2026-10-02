# NB05 — Translation Ingestion and Acceptance

## Status
`PENDING_LOCAL_RUN_ALL`

## Purpose
Create deterministic verse-aligned translation JSONL artifacts while keeping them quarantined for internal research until source-specific republication rights are verified.

## Outputs
- `data/phase1/processed/translations/fa.fooladvand_v1.jsonl`
- `data/phase1/processed/translations/fa.ansarian_v1.jsonl`
- `artifacts/phase1/translations/translation_manifest_v1.json`
- `reports/phase1/translation_ingestion_acceptance_v1.json`

## Key design
Artifact creation and source activation are separate operations.

# NB03 — Quran Canonical Ingestion and Acceptance

## Status
`PENDING_LOCAL_RUN_ALL`

## Purpose
Create a deterministic 6236-record canonical Quran JSONL with one stable verse ID per record and exact raw-text fidelity.

## Output
- `data/phase1/processed/quran_canonical_v1.jsonl`
- `artifacts/phase1/quran/quran_canonical_manifest_v1.json`
- `reports/phase1/quran_canonical_ingestion_acceptance_v1.json`

## Non-negotiable rule
The canonical `arabic_uthmani` field is a verbatim structured copy of the accepted raw verse text. Search normalization is forbidden here.

## Known limitation
The original remote download fingerprint is unavailable from legacy history; the local raw SHA-256 is frozen and tied to documented Tanzil provenance.

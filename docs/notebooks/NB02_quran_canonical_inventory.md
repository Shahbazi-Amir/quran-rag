# NB02 — Quran Canonical Inventory

## Status
`PENDING_LOCAL_RUN_ALL`

## Purpose
Audit structural identity, verse numbering, local raw hash and official Tanzil source/license evidence for the existing Uthmani file.

## Important decisions
- Expected verse count: 6236 across 114 surahs.
- Raw verse text is not normalized.
- Tanzil official documentation is the source for text-license evidence.
- The historical remote download checksum was not preserved by the legacy notebook, so the local raw SHA-256 becomes a frozen lineage anchor after NB02.

## Outputs after local execution
- `reports/phase1/quran_canonical_inventory_v1.json`
- `reports/phase1/quran_canonical_inventory_acceptance_v1.json`

## Failure path
Do not run NB03 if verse keys, ordering, counts, duplicates or malformed lines fail.

# QRAG Phase 1 — Wave 01 Task Register

**Branch:** `qrag-phase1`  
**Wave:** 01  
**Tasks:** 001–100  
**Scope:** Foundation, repository audit, source authority, NB00, NB01  

## وضعیت موج

تمام 100 Task تعریف‌شده این موج اجرا شده‌اند. این جمله به معنی PASS نهایی NB00/NB01 روی Mac کاربر نیست. اجرای واقعی `Restart Kernel → Run All` روی clone پروژه همچنان Gate بیرونی لازم است؛ اجرای Synthetic هر دو Notebook انجام شده است.

| ID | Task | Status | Evidence |
|---:|---|---|---|
| 001 | Create isolated qrag-phase1 branch | DONE | branch:qrag-phase1 |
| 002 | Bind Phase 1 baseline to original main commit | DONE | baseline:059b8f22fa2ab4d9f62c5b7d978debc5d79e41b3 |
| 003 | Keep main outside Phase 1 writes | DONE | branch policy documented |
| 004 | Record RAG_finance as read-only architecture reference | DONE | master roadmap |
| 005 | Inventory repository tree and legacy assets | DONE | repository audit |
| 006 | Audit legacy Streamlit app architecture | DONE | repository audit |
| 007 | Inventory existing Quran/translation/embedding files | DONE | repository audit |
| 008 | Inventory legacy notebooks 01-09 | DONE | repository audit |
| 009 | Audit existing test files | DONE | repository audit |
| 010 | Audit empty/placeholder config and package files | DONE | repository audit |
| 011 | Create QRAG Phase 1 master roadmap | DONE | Q_RAG_PHASE1_MASTER_ROADMAP.md |
| 012 | Create Phase 1 operational roadmap | DONE | Q_RAG_PHASE1_OPERATIONAL_ROADMAP.md |
| 013 | Create notebook execution contract | DONE | Q_RAG_PHASE1_NOTEBOOK_EXECUTION_PLAN.md |
| 014 | Create documentation standard | DONE | Q_RAG_PHASE1_DOCUMENTATION_STANDARD.md |
| 015 | Create 15-wave / 1500-task execution plan | DONE | Q_RAG_PHASE1_TASK_WAVES.md |
| 016 | Define epistemic source-layer model | DONE | source_authority_policy_v1.json |
| 017 | Define canonical Quran layer | DONE | source authority policy |
| 018 | Define translation layer | DONE | source authority policy |
| 019 | Define tafsir layer | DONE | source authority policy |
| 020 | Define hadith layer | DONE | source authority policy |
| 021 | Define derived-claim layer | DONE | source authority policy |
| 022 | Define generated-answer layer | DONE | source authority policy |
| 023 | Define Quran-only answer mode | DONE | source authority policy |
| 024 | Define Quran-with-translation answer mode | DONE | source authority policy |
| 025 | Define tafsir-assisted answer mode | DONE | source authority policy |
| 026 | Define hadith-assisted answer mode | DONE | source authority policy |
| 027 | Define scholarly-synthesis answer mode | DONE | source authority policy |
| 028 | Define disagreement/conflict relation vocabulary | DONE | source authority policy |
| 029 | Define quarantine rule for unverified rights | DONE | source authority policy |
| 030 | Reject repository presence as rights evidence | DONE | source authority policy |
| 031 | Define Quran citation minimum locator | DONE | source authority policy |
| 032 | Define translation citation minimum locator | DONE | source authority policy |
| 033 | Define tafsir citation minimum locator | DONE | source authority policy |
| 034 | Define hadith citation minimum locator | DONE | source authority policy |
| 035 | Define derived-claim citation contract | DONE | source authority policy |
| 036 | Prohibit question-specific manual answer injection | DONE | source authority policy |
| 037 | Document Shia-priority discovery scope without auto-acceptance | DONE | source authority policy |
| 038 | Create source-candidate manifest | DONE | source_candidates_v1.json |
| 039 | Register legacy Uthmani Quran candidate | DONE | source candidate manifest |
| 040 | Register Fooladvand translation candidate | DONE | source candidate manifest |
| 041 | Register Ansarian translation candidate | DONE | source candidate manifest |
| 042 | Register Al-Mizan tafsir candidate | DONE | source candidate manifest |
| 043 | Register Tasnim tafsir candidate | DONE | source candidate manifest |
| 044 | Register Tafsir Nemuneh candidate | DONE | source candidate manifest |
| 045 | Register Nur al-Thaqalayn riwayi-tafsir candidate | DONE | source candidate manifest |
| 046 | Register Al-Burhan riwayi-tafsir candidate | DONE | source candidate manifest |
| 047 | Register Al-Kafi hadith candidate | DONE | source candidate manifest |
| 048 | Register Man La Yahduruhu al-Faqih candidate | DONE | source candidate manifest |
| 049 | Register Tahdhib al-Ahkam candidate | DONE | source candidate manifest |
| 050 | Register Al-Istibsar candidate | DONE | source candidate manifest |
| 051 | Register Nahj al-Balagha candidate | DONE | source candidate manifest |
| 052 | Register Sahifa Sajjadiya candidate | DONE | source candidate manifest |
| 053 | Create machine-readable source-record JSON Schema | DONE | source_record.schema.json |
| 054 | Require stable source_id | DONE | source schema |
| 055 | Constrain source_family vocabulary | DONE | source schema |
| 056 | Constrain epistemic_layer vocabulary | DONE | source schema |
| 057 | Constrain rights_status vocabulary | DONE | source schema |
| 058 | Constrain acceptance_status vocabulary | DONE | source schema |
| 059 | Constrain acquisition_status vocabulary | DONE | source schema |
| 060 | Require non-empty source validation checks | DONE | source schema |
| 061 | Create Phase 1 Python package namespace | DONE | src/qrag_phase1/__init__.py |
| 062 | Implement deterministic SHA-256 helper | DONE | foundation.py |
| 063 | Implement read-only Git command helper | DONE | foundation.py |
| 064 | Implement Git baseline collector | DONE | foundation.py |
| 065 | Implement repository inventory collector | DONE | foundation.py |
| 066 | Implement atomic JSON writer | DONE | foundation.py |
| 067 | Test SHA-256 determinism | DONE | test_foundation.py |
| 068 | Test atomic JSON round-trip | DONE | test_foundation.py |
| 069 | Test repository inventory helper | DONE | test_foundation.py |
| 070 | Test Git baseline collector in temporary repository | DONE | test_foundation.py |
| 071 | Execute foundation unit-test suite | DONE | 4/4 tests PASS |
| 072 | Create NB00 objective/scope markdown | DONE | NB00 |
| 073 | Create NB00 execution-plan markdown | DONE | NB00 |
| 074 | Implement NB00 runtime-environment cell | DONE | NB00-C01 |
| 075 | Implement NB00 dynamic project-root cell | DONE | NB00-C02 |
| 076 | Implement NB00 Git-baseline cell | DONE | NB00-C03 |
| 077 | Implement NB00 repository-inventory cell | DONE | NB00-C04 |
| 078 | Implement NB00 legacy-notebook health audit | DONE | NB00-C05 |
| 079 | Implement NB00 baseline-data inventory and hashing | DONE | NB00-C06 |
| 080 | Implement NB00 dependency/secret-presence contract | DONE | NB00-C07 |
| 081 | Implement NB00 versioned baseline report | DONE | NB00-C08 |
| 082 | Implement NB00 independent disk reload validation | DONE | NB00-C09 |
| 083 | Implement NB00 machine-readable acceptance report | DONE | NB00-C10 |
| 084 | Document NB00 final interpretation and limitations | DONE | NB00-M12 |
| 085 | Create NB00 companion troubleshooting document | DONE | NB00_environment_and_baseline.md |
| 086 | Execute NB00 end-to-end in synthetic Git repository | DONE | synthetic Restart/Run All PASS |
| 087 | Create NB01 purpose/scope documentation | DONE | NB01 |
| 088 | Document non-negotiable source-authority rules | DONE | NB01-M02 |
| 089 | Implement NB01 root and input-contract loading | DONE | NB01-C01/C02 |
| 090 | Implement NB01 source-policy validation | DONE | NB01-C03 |
| 091 | Implement NB01 candidate-manifest validation | DONE | NB01-C04 |
| 092 | Implement NB01 repository-backed candidate check | DONE | NB01-C05 |
| 093 | Implement NB01 Shia-priority/no-auto-acceptance gate | DONE | NB01-C06 |
| 094 | Implement NB01 citation-contract validation | DONE | NB01-C07 |
| 095 | Implement NB01 conflict-preservation validation | DONE | NB01-C08 |
| 096 | Implement NB01 machine-readable acceptance report | DONE | NB01-C09 |
| 097 | Implement NB01 final health gate | DONE | NB01-C10 |
| 098 | Create NB01 companion troubleshooting document | DONE | NB01_source_policy_rights_and_authority.md |
| 099 | Execute NB01 end-to-end in synthetic Git repository | DONE | synthetic Restart/Run All PASS_WITH_LIMITATIONS |
| 100 | Run Wave 01 audit and identify next hard gate | DONE | wave01 audit; real local Run All remains required |

## نتیجه

- Taskهای انجام‌شده: 100/100
- Unit tests: 4/4 PASS
- NB00 Synthetic Restart/Run All: PASS
- NB01 Synthetic Restart/Run All: PASS_WITH_LIMITATIONS
- Local real-repository NB00/NB01: PENDING_LOCAL_RUN_ALL
- Sourceهای Active پس از Wave 01: 0
- Candidateهای ثبت‌شده: 14
- مرحله بعد پس از Local Gate: NB02 — Quran Canonical Inventory

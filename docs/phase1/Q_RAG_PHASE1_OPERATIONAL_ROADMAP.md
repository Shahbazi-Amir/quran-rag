# نقشه عملیاتی فاز یک QRAG

## سیاست اجرا
فاز یک به Notebookهای مستقل تقسیم می‌شود. هر Notebook یک مأموریت روشن، ورودی نسخه‌دار، خروجی نسخه‌دار، تست، Acceptance Gate و فایل مستند همراه دارد.

## Notebookهای برنامه‌ریزی‌شده
00. environment_and_baseline
01. source_policy_rights_and_authority
02. quran_canonical_inventory
03. quran_canonical_ingestion_and_acceptance
04. translation_inventory
05. translation_ingestion_and_acceptance
06. tafsir_inventory
07. tafsir_ingestion_and_acceptance
08. hadith_inventory
09. hadith_ingestion_and_acceptance
10. unified_schema_and_lineage
11. arabic_persian_normalization
12. deduplication_and_quality
13. verse_source_alignment_and_locators
14. quranic_taxonomy_and_knowledge_engineering
15. claim_extraction
16. claim_registry_relations_and_knowledge_graph
17. chunking_benchmark
18. golden_dataset
19. embedding_benchmark
20. dense_index
21. sparse_index
22. hybrid_retrieval
23. reranking
24. question_understanding_and_query_decomposition
25. context_builder
26. generation_and_claim_level_citation
27. answerability_conflict_safety_confidence
28. evaluation_ablation_and_regression
29. release_reproducibility_and_application_handoff

## Gateهای کلان
### Gate A — Foundation
NB00–NB01
محیط، Branch، Commit، وابستگی‌ها، سیاست منبع، اعتبار، حقوق و حدود استفاده ثبت شده باشند.

### Gate B — Source Foundation
NB02–NB09
قرآن، ترجمه، تفسیر و حدیث دارای Inventory، Stable ID، provenance و Acceptance باشند.

### Gate C — Canonical Knowledge Layer
NB10–NB16
Schema، Lineage، Normalization، Quality، Alignment، Taxonomy و Claim Registry پایدار باشند.

### Gate D — Retrieval
NB17–NB23
Chunking و Embedding با Benchmark انتخاب شده و Dense/Sparse/Hybrid/Reranking فریز شده باشند.

### Gate E — Reasoning and Answering
NB24–NB27
فهم سؤال، Context Builder، Generation، Citation، Conflict handling و Answerability کار کنند.

### Gate F — Release
NB28–NB29
Evaluation، Ablation، Regression و Reproducibility پاس شده باشند.

## Fail-closed rule
اگر یک Gate بنیادی FAIL شود، downstream ادامه پیدا نمی‌کند مگر اینکه:
- Failure ثبت شود؛
- علت فنی روشن شود؛
- Repair انجام شود؛
- Validation مستقل دوباره PASS شود.

## سیاست منبع
### قرآن
canonical primary source

### ترجمه
translation source؛ ترجمه برابر با متن عربی نیست.

### تفسیر
interpretive scholarly source؛ نام مفسر، اثر، جلد/بخش/آیه و نسخه باید حفظ شود.

### حدیث
narrative source؛ collection/book/chapter/hadith identifier و grading فقط در صورت وجود منبع معتبر ذخیره می‌شود. درجه حدیث توسط مدل ساخته نمی‌شود.

## سیاست اختلاف
Agreement، Complement، Partial Overlap، Difference و Conflict باید قابل ثبت باشند. سیستم نباید اختلاف تفاسیر یا روایات را با Merge خودکار حذف کند.

## سیاست پایگاه داده
در فاز یک انتخاب Database از قبل تحمیل نمی‌شود.
- Artifactهای truth باید قابل version و hash باشند.
- Vector index فقط بعد از Benchmark انتخاب می‌شود.
- PostgreSQL فقط اگر نیاز عملیاتی واقعی فاز یک آن را توجیه کند وارد می‌شود.
- اطلاعات منبع و lineage نباید وابسته به یک DB غیرقابل بازسازی باشند.

## سیاست مدل
هیچ انتخاب Embedding، Reranker یا LLM صرفاً بر اساس شهرت مدل انجام نمی‌شود. هر انتخاب باید حداقل با Development benchmark، latency، memory footprint و limitations ثبت شود.

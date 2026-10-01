# برنامه موج‌های کاری فاز یک QRAG

## اندازه اولیه Backlog
Backlog اولیه: حدود 1500 Task اتمیک.

این عدد Contract ثابت نیست. پس از Source Inventory و اولین Audit می‌تواند افزایش یا کاهش یابد، اما هر تغییر باید دلیل مستند داشته باشد.

## تعریف Task اتمیک
Task باید خروجی قابل بررسی داشته باشد. نمونه:
- تعریف یک Schema field
- ساخت validator برای یک Contract
- استخراج یک Inventory
- ساخت یک fixture
- اجرای یک benchmark
- تحلیل یک failure mode
- ساخت یک acceptance check
- تکمیل یک مستند تصمیم

کار بسیار ریز و مصنوعی Task مستقل محسوب نمی‌شود.

## موج‌ها
- Wave 01: Tasks 001–100 — Foundation, audit, roadmaps, source policy, NB00/NB01 start
- Wave 02: Tasks 101–200 — Quran canonical source
- Wave 03: Tasks 201–300 — Translation inventory and ingestion
- Wave 04: Tasks 301–400 — Tafsir inventory
- Wave 05: Tasks 401–500 — Tafsir ingestion and acceptance
- Wave 06: Tasks 501–600 — Hadith inventory
- Wave 07: Tasks 601–700 — Hadith ingestion and acceptance
- Wave 08: Tasks 701–800 — Unified schema, lineage, normalization
- Wave 09: Tasks 801–900 — Quality, alignment, taxonomy
- Wave 10: Tasks 901–1000 — Claim extraction and registry
- Wave 11: Tasks 1001–1100 — Chunking and Golden Dataset
- Wave 12: Tasks 1101–1200 — Embedding, dense and sparse retrieval
- Wave 13: Tasks 1201–1300 — Hybrid, reranking, question understanding
- Wave 14: Tasks 1301–1400 — Context, generation, citation, answerability
- Wave 15: Tasks 1401–1500 — Evaluation, ablation, regression, release

## Audit بعد از هر موج
هر Wave با یک Audit بسته می‌شود:
1. چه Taskهایی واقعاً Done شدند؟
2. چه Taskهایی Blocked شدند؟
3. کدام Artifactها ساخته شدند؟
4. کدام Notebookها PASS شدند؟
5. چه محدودیت‌هایی باز هستند؟
6. چه تفاوتی با معماری RAG_finance وجود دارد؟
7. آیا Wave بعدی مجاز است؟

## Stop conditions
ادامه کار متوقف می‌شود اگر:
- منبع اصلی قابل شناسایی نباشد؛
- حقوق/اجازه استفاده مبهم و برای مرحله بعد حیاتی باشد؛
- mapping آیه/منبع ناسالم باشد؛
- Hash یا Lineage شکسته باشد؛
- Test leakage رخ دهد؛
- API پولی لازم باشد ولی مجوز هزینه روشن نباشد؛
- اجرای محلی الزامی باشد و هنوز Run All تأیید نشده باشد.

## Wave 01 — خروجی مورد انتظار
- Branch مستقل Phase 1
- Audit اولیه Repository
- پنج سند اصلی Phase 1
- تعریف Documentation Contract
- تعریف Notebook Contract
- تعریف Source Authority Model
- شروع Notebook 00
- Acceptance report اولیه

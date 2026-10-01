# استاندارد مستندسازی فاز یک QRAG

## هدف
مستندات باید به شکلی باشند که در هر زمان بتوان فهمید:
- سیستم کجاست؛
- چه چیزی وارد شده؛
- چه تصمیمی گرفته شده؛
- چرا گرفته شده؛
- چه چیزی شکست خورده؛
- برای اصلاح باید به کدام Notebook یا Module رفت.

## حداقل فایل‌ها
برای جلوگیری از انفجار فایل، فقط این لایه‌ها اجباری هستند:
1. Roadmapهای اصلی در `docs/phase1/`
2. یک MD برای هر Notebook در `docs/notebooks/`
3. گزارش‌های ماشین‌خوان Acceptance در `reports/phase1/`
4. Artifactهای فنی در `artifacts/phase1/`
5. کد پایدار در `src/`

برای هر تصمیم کوچک فایل جدا ساخته نمی‌شود.

## اصل Single Source of Truth
- Roadmap: مسیر و Scope
- Notebook: تاریخچه اجرایی و آزمایش
- Notebook MD: خلاصه عملیاتی و راه عیب‌یابی
- Acceptance JSON: وضعیت ماشین‌خوان
- Artifact: خروجی نسخه‌دار
- Source code: منطق پایدار

## ثبت Provenance
برای هر منبع حداقل:
- source_id
- source_type
- title
- creator/author/scholar
- edition/version
- original locator
- acquisition source
- acquisition date
- raw hash
- rights status
- allowed use
- attribution text
- pipeline version

## ثبت تصمیم
هر تصمیم مهم داخل Notebook و MD همراه باید شامل:
- مسئله
- گزینه‌ها
- شواهد
- تصمیم
- محدودیت
- شرط بازنگری

## Commit policy
Commitها باید کوچک و معنایی باشند.
نمونه:
- `docs(phase1): add QRAG master and operational roadmaps`
- `feat(nb02): add canonical Quran inventory`
- `test(nb02): add verse count and checksum validation`
- `fix(nb07): repair tafsir locator lineage`

هر Commit باید با مستندات مرتبط هماهنگ باشد.

## وضعیت‌های استاندارد
- DRAFT
- IN_PROGRESS
- BLOCKED
- PASS
- PASS_WITH_LIMITATIONS
- FAIL
- FROZEN
- PENDING_LOCAL_RUN_ALL

## Audit cadence
بعد از هر موج 100 Task:
- Repository audit
- Notebook health
- Artifact integrity
- lineage audit
- comparison with relevant RAG_finance architecture
- open risks
- task reprioritization

بعد از هر 500 Task:
- architecture audit
- source strategy review
- evaluation leakage review
- documentation consistency review

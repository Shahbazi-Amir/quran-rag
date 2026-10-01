# NB00 — Environment and Baseline

## Status
`PENDING_LOCAL_RUN_ALL`

## Purpose
ثبت Environment، Git baseline، Repository inventory، Legacy notebook health، داده‌های موجود و Dependency contract بدون تغییر محتوایی Corpus.

## Inputs
- Repository clone روی `qrag-phase1`
- Raw files موجود
- Notebookهای Legacy
- `requirements.txt`
- Environment variable presence

## Outputs
پس از اجرای واقعی:
- `reports/phase1/environment_baseline_v1.json`
- `reports/phase1/environment_baseline_acceptance_v1.json`

## Tests انجام‌شده
- Syntax تمام Code Cellها خارج از Repository واقعی بررسی شد.
- Helper module با 4 Unit Test مستقل PASS شد.
- Notebook کامل در Synthetic Git Repository با همان Branch contract اجرا شد و PASS کرد.
- Atomic write و Reload validation در اجرای Synthetic PASS شد.

## چرا هنوز PASS نهایی نیست؟
اجرای Synthetic صحت منطق Notebook را نشان می‌دهد، اما Hash، مسیر، نسخه Python، Dependencyها و Git state سیستم واقعی کاربر را اثبات نمی‌کند. بنابراین تا `Restart Kernel → Run All` روی clone واقعی وضعیت نهایی PASS اعلام نمی‌شود.

## Known limitations
- Legacy processed dataset در Git موجود نیست.
- Legacy NB09 سه Code Cell اجرا‌نشده دارد.
- Source provenance سه فایل موجود هنوز پذیرفته نشده و از NB02 به بعد بررسی می‌شود.

## Repair path
اگر NB00 Fail شود:
1. ابتدا Cell دقیق Fail را مشخص کن.
2. Root/Branch/Input contract را بررسی کن.
3. فقط NB00 یا helper مربوط اصلاح شود.
4. Restart Kernel → Run All دوباره اجرا شود.
5. تا PASS شدن NB00 وارد Source ingestion نشو.

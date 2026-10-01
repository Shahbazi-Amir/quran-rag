# ممیزی اولیه Repository برای QRAG Phase 1

## Scope
این ممیزی روی Repository `Shahbazi-Amir/quran-rag` انجام شده و وضعیت موجود قبل از بازطراحی حرفه‌ای را ثبت می‌کند.

Branch توسعه: `qrag-phase1`

Baseline اولیه Branch از Commit:
`059b8f22fa2ab4d9f62c5b7d978debc5d79e41b3`

## یافته‌های اصلی
- `main` به‌عنوان Baseline قدیمی دست‌نخورده نگه داشته می‌شود.
- `app.py` نسخه Legacy 0.3.0 است و Query Expansion دستی برای برخی سؤال‌ها دارد.
- سه فایل Raw موجودند: قرآن عثمانی، ترجمه فولادوند و ترجمه انصاریان.
- Embedding قدیمی `quran_embeddings.npy` موجود است.
- فایل `data/processed/quran_dataset_clean.json` در Git Tree موجود نیست، در حالی که Legacy app آن را انتظار دارد؛ بنابراین fresh clone نسخه Legacy به Artifact محلی وابسته است.
- دو Cache JSON در Git Track شده‌اند و بخشی از Legacy state هستند.
- `README.md` تقریباً خالی است.
- `requirements.txt` و `.env.example` در Baseline اولیه خالی بودند.
- فایل‌های `app/config.py`، `app/main.py` و `app/rag.py` خالی بودند.
- تست‌های Legacy `tests/test_data.py` و `tests/test_retrieval.py` خالی بودند.
- `.gitignore` شامل متن Shell wrapper بود و در Branch Phase 1 اصلاح شد.

## سلامت Notebookهای Legacy
Audit خواندنی GitHub نشان داد:
- NB01: 9 Cell، Error Output صفر، Code Cell اجرا‌نشده صفر.
- NB02: 10 Cell، Error Output صفر، Code Cell اجرا‌نشده صفر.
- NB03: 12 Cell، Error Output صفر، Code Cell اجرا‌نشده صفر.
- NB04: 15 Cell، Error Output صفر، Code Cell اجرا‌نشده صفر.
- NB05: 12 Cell، Error Output صفر، Code Cell اجرا‌نشده صفر.
- NB06: 20 Cell، Error Output صفر، Code Cell اجرا‌نشده صفر.
- NB07: 12 Cell، Error Output صفر، Code Cell اجرا‌نشده صفر.
- NB08: 21 Cell، Error Output صفر، Code Cell اجرا‌نشده صفر.
- NB09: 9 Cell و 3 Code Cell اجرا‌نشده؛ Error Output ثبت‌شده صفر.

این آمار فقط سلامت فایل‌های ذخیره‌شده را نشان می‌دهد و جایگزین اجرای مجدد از Kernel پاک نیست.

## تصمیم معماری
دارایی‌های Legacy حذف نمی‌شوند و به‌عنوان Baseline تاریخی باقی می‌مانند، اما:
- هیچ Raw file موجود بدون Source audit به‌عنوان Canonical پذیرفته نمی‌شود.
- Embedding قدیمی فقط Reference است و انتخاب مدل Phase 1 محسوب نمی‌شود.
- Query Expansion سؤال‌محور دستی، معماری نهایی نیست.
- Notebookهای حرفه‌ای جدید از `notebooks/phase1/00...` شروع می‌شوند.

## محدودیت ممیزی
Connector GitHub امکان اجرای Notebook روی Mac واقعی پروژه را نمی‌دهد. برای همین Static audit و Synthetic execution جدا از Local Restart/Run All ثبت می‌شوند.

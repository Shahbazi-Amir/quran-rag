# قرارداد اجرای Notebookهای فاز یک QRAG

## هدف
این سند قالب اجباری هر Notebook را تعریف می‌کند تا پروژه برای انسان، Agent و توسعه‌دهنده بعدی قابل فهم و قابل بازتولید بماند.

## ساختار اجباری هر Notebook
هر Notebook باید با Markdown شروع شود:

### Markdown 01 — هویت و هدف
- نام Notebook
- هدف دقیق
- چرا این مرحله لازم است
- ورودی‌ها
- خروجی‌ها
- خارج از Scope
- معیار PASS/FAIL

### Markdown 02 — برنامه اجرای مرحله
- Cellهای مورد انتظار
- وابستگی به Notebookهای قبلی
- Artifactهایی که خوانده می‌شوند
- Artifactهایی که ممکن است نوشته شوند

### Code Cell 01 — Imports و Environment
- فقط importهای لازم
- چاپ نکردن Secret
- بررسی نسخه‌های حیاتی در صورت نیاز

### Code Cell 02 — Project Root / Input Contract
- کشف Root بدون مسیر hard-coded شخصی
- بررسی وجود ورودی
- Schema/version/hash validation

### Code Cellهای میانی
هر بخش باید یک وظیفه مستقل داشته باشد و قبل از Code Cell مربوط، Markdown توضیحی کوتاه داشته باشد.

### Validation Cells
- assertهای واقعی
- integrity check
- count parity
- hash validation
- schema validation
- عدم اتکا صرف به print

### Final Acceptance Cell
باید نتیجه ماشین‌خوان تولید کند:
- objective_status
- acceptance_status
- failed_checks
- warnings
- artifact paths
- hashes
- next_notebook

### Final Markdown — جمع‌بندی
- چه چیزی انجام شد
- چه چیزی انجام نشد
- محدودیت‌ها
- آیا هدف Notebook محقق شد
- مرحله بعد چیست

## قرارداد شماره‌گذاری
Code Cellها:
`NB00-C01`, `NB00-C02`, ...

Markdown sectionها:
`NB00-M01`, `NB00-M02`, ...

## فایل مستند همراه
برای هر Notebook یک فایل مستقل در این مسیر ساخته می‌شود:

`docs/notebooks/NBxx_<name>.md`

این فایل حداقل شامل:
- Purpose
- Inputs
- Outputs
- Important decisions
- Tests
- Acceptance result
- Known limitations
- Repair notes
- Commit/Artifact references

Notebook سند اجرایی تفصیلی است؛ فایل MD نمای سریع معماری و عیب‌یابی است.

## معیار تحویل Notebook
Notebook تمام‌شده محسوب نمی‌شود مگر اینکه:
1. Syntax error نداشته باشد.
2. Cell اجرا‌نشده ناخواسته نداشته باشد.
3. Error output باقی‌مانده نداشته باشد.
4. از Kernel پاک قابلیت Run All داشته باشد یا دلیل محیطی مستند داشته باشد.
5. Acceptance Cell اجرا شده باشد.
6. MD همراه به‌روزرسانی شده باشد.
7. Artifactهای نوشته‌شده دوباره از Disk خوانده و Validation شده باشند.
8. تغییرات Commit شده باشند.

## اجرای محلی و Agent
هرجا محیط Connector امکان اجرای واقعی Python/Jupyter ندهد، کد «تأییدشده» اعلام نمی‌شود. در این حالت:
- من Static validation و repository checks را انجام می‌دهم.
- Notebook با وضعیت `PENDING_LOCAL_RUN_ALL` تحویل می‌شود.
- کاربر Pull می‌کند و `Restart Kernel → Run All` اجرا می‌کند.
- Output واقعی مبنای PASS نهایی قرار می‌گیرد.

هیچ Notebook صرفاً به دلیل ظاهر درست کد PASS نمی‌شود.

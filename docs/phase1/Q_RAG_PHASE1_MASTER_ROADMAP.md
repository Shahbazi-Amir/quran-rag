# نقشه کلان فاز یک QRAG

## تعریف پروژه
نام پروژه: QRAG — Quranic Retrieval-Augmented Generation

شاخه اجرایی: `qrag-phase1`

هدف فاز یک، ساخت یک هسته حرفه‌ای، قابل ردیابی، قابل ارزیابی و قابل توسعه برای پرسش و پاسخ قرآنی است؛ به‌گونه‌ای که متن قرآن، ترجمه، تفسیر، حدیث، ادعاهای استخراج‌شده و پاسخ مدل در لایه‌های جدا و قابل ممیزی نگهداری شوند.

## اصول ثابت
- `main` در این فاز تغییر نمی‌کند.
- مخزن `RAG_finance` فقط مرجع خواندنی معماری است و نباید تغییر کند.
- Notebookها مستند اجرایی پروژه هستند، نه محل انباشتن منطق پایدار.
- منطق پایدار باید در Python moduleهای نسخه‌دار قرار گیرد و Notebookها آن را اجرا، تست و مستند کنند.
- هر Notebook باید از Kernel پاک با Restart & Run All قابل اجرا باشد.
- هر خروجی مهم باید Version، Hash، Lineage و Acceptance status داشته باشد.
- متن قرآن، ترجمه، تفسیر، حدیث و استنباط مدل هرگز یک سطح معرفتی محسوب نمی‌شوند.
- هیچ منبعی قبل از بررسی هویت، نسخه، حقوق استفاده و قابلیت Citation وارد Corpus فعال نمی‌شود.
- هیچ Claim بدون Evidence نهایی پذیرفته نمی‌شود.
- Golden Dataset منبع پاسخ نیست؛ ابزار ارزیابی سیستم است.

## لایه‌های دانش
1. قرآن عربی canonical
2. ترجمه‌های قرآن
3. تفاسیر
4. منابع حدیثی و روایی
5. Claim Registry و روابط دانشی
6. Retrieval Context
7. پاسخ تولیدشده

## خانواده‌های منبع کاندید
### قرآن
- متن عثمانی موجود در Repository
- هر متن جایگزین فقط پس از Verse-count، checksum، numbering و source audit

### ترجمه
- فولادوند
- انصاریان
- ترجمه‌های دیگر در صورت پذیرش حقوقی و فنی
- هر مترجم به‌عنوان Source مستقل و بدون ادغام خاموش

### تفسیر
اولویت پژوهشی:
- المیزان
- تسنیم
- نمونه
- سایر تفاسیر شیعی فقط پس از Inventory و Acceptance

### حدیث و منابع روایی
اولویت با منابع شیعی و نسخه‌های دارای شناسه و ساختار قابل استناد است.
کاندیدها می‌توانند شامل کتب اربعه، نهج‌البلاغه، صحیفه سجادیه و منابع تفسیری روایی باشند، اما هیچ موردی پیشاپیش پذیرفته‌شده محسوب نمی‌شود.

## معماری هدف
```text
Question
  ↓
Question Understanding
  ↓
Intent / Concepts / Ambiguity / Decomposition
  ↓
Quran + Translation + Tafsir + Hadith Retrieval
  ↓
Claim / Evidence Retrieval
  ↓
Dense + Sparse
  ↓
Hybrid Retrieval
  ↓
Reranking
  ↓
Authority-aware Context Builder
  ↓
Grounded Generation
  ↓
Claim-level Citation
  ↓
Answerability / Conflict / Confidence / Abstention
  ↓
Answer + Exact Provenance
```

## خروجی فاز یک
فاز یک زمانی Done است که:
- Corpusهای پذیرفته‌شده نسخه‌دار و قابل بازسازی باشند.
- هر رکورد به Raw source و provenance برگردد.
- Question understanding عمومی باشد و مبتنی بر Ruleهای سؤال‌محور دستی نباشد.
- Dense، Sparse، Hybrid و Reranking با Benchmark مقایسه شده باشند.
- پاسخ‌ها Claim-level Citation داشته باشند.
- اختلاف منابع به‌صورت قابل مشاهده حفظ شود.
- سؤال‌های بی‌پاسخ و مبهم به‌درستی Abstain یا Clarify شوند.
- Golden Dev/Test و Regression Gate وجود داشته باشد.
- Release نهایی از محیط تمیز قابل بازتولید باشد.

## فاز دو آینده
فاز دو بر مبنای ممیزی فاز یک تعریف خواهد شد و پیشاپیش Freeze نمی‌شود. هدف آن اصلاح ضعف‌های اندازه‌گیری‌شده فاز یک، سخت‌سازی معماری و توسعه قابلیت‌هایی است که Benchmark و Audit ضرورت آن‌ها را اثبات کنند.

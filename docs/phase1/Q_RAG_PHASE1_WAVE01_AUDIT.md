# QRAG Phase 1 — Wave 01 Audit

## نتیجه اجرایی
Wave 01 شامل Taskهای 001 تا 100 تکمیل شد.

این موج Foundation پروژه را ساخته است: Roadmapها، استاندارد مستندسازی، Audit مخزن، Python helperها، Unit Testها، Source Authority Policy، Candidate Manifest، NB00 و NB01.

## Test Evidence
- Foundation unit tests: **4/4 PASS**
- NB00 در Synthetic Git repository با Branch واقعی مورد انتظار: **PASS**
- NB01 در Synthetic Git repository: **PASS_WITH_LIMITATIONS**
- NB01 عمداً هیچ Source را Active نکرده است.

## محدودیت مهم
Synthetic execution جای اجرای واقعی روی Mac و فایل‌های واقعی Repository را نمی‌گیرد. بنابراین NB00 و NB01 هنوز در مستندهای همراه با وضعیت `PENDING_LOCAL_RUN_ALL` نگه داشته شده‌اند.

## چرا این توقف درست است؟
NB02 قرار است متن قرآن موجود را Canonical audit کند. اگر Baseline واقعی محیط یا Source Policy روی سیستم واقعی Fail شود، رفتن به NB02 می‌تواند Lineage غلط بسازد. پس معماری Fail-Closed حفظ می‌شود.

## Gate کاربر
روی Branch `qrag-phase1` Pull کن و به ترتیب این دو Notebook را اجرا کن:

1. `notebooks/phase1/00_environment_and_baseline.ipynb`
2. `notebooks/phase1/01_source_policy_rights_and_authority.ipynb`

برای هر کدام:
`Restart Kernel → Run All`

اگر هر دو بدون Error تمام شدند، خروجی Final Acceptance Cellها را بفرست. بعد Wave 02 / NB02 را بدون بازطراحی Foundation شروع می‌کنیم.

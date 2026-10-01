# NB01 — Source Policy, Rights and Authority

## Status
`PENDING_LOCAL_RUN_ALL`

## Purpose
تعریف مرز رسمی میان قرآن، ترجمه، تفسیر، حدیث، Claim و پاسخ تولیدشده و جلوگیری از ورود Source بدون Provenance/Edition/Rights/Citation contract.

## Contractهای اصلی
- `config/phase1/source_authority_policy_v1.json`
- `schemas/phase1/source_record.schema.json`
- `data/phase1/manifests/source_candidates_v1.json`

## Candidateهای اولیه
14 Candidate ثبت شده‌اند:
- 1 متن قرآن موجود در Repository
- 2 ترجمه موجود
- 5 تفسیر Candidate، شامل المیزان، تسنیم، نمونه و دو منبع تفسیری روایی شیعی
- 6 منبع حدیثی/روایی Candidate

هیچ‌یک هنوز `accepted` نیستند.

## سیاست مهم
- اولویت Tafsir/Hadith شیعی فقط Discovery را هدایت می‌کند.
- نام مشهور منبع دلیل پذیرش نیست.
- `rights_status=evidence_required` یعنی Source تا قبل از Evidence وارد Active Corpus نمی‌شود.
- مدل حق تولید grading حدیث ندارد.
- اختلاف منابع باید حفظ شود.

## Tests انجام‌شده
- یکتایی Source ID.
- سازگاری Source family و epistemic layer.
- جلوگیری از Premature acceptance.
- صحت Repository path برای سه Candidate موجود.
- Citation contract.
- Conflict relation contract.
- Synthetic Restart/Run All با 14 Candidate PASS شد.
- Acceptance مصنوعی نتیجه `PASS_WITH_LIMITATIONS` داد چون 11 Source خارجی هنوز acquire نشده و حقوق هر 14 Candidate نیازمند Evidence است.

## Output پس از اجرای واقعی
- `reports/phase1/source_policy_acceptance_v1.json`

## Next
NB02 فقط Canonical inventory قرآن موجود را شروع می‌کند؛ Tafsir/Hadith ingestion هنوز مجاز نیست.

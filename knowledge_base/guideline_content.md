# IRBM e-Invoice Guideline (Version 4.6) - Knowledge Base

## 1.0 INTRODUCTION

e-Invoice is implemented in stages to enhance efficiency of Malaysia's tax administration. It enables near real-time validation and storage for B2B, B2C and B2G transactions.

### 1.1 About e-Invoice
- e-Invoice is a digital representation of a transaction between supplier and buyer.
- Replaces paper/electronic documents: invoices, credit notes, debit notes.
- Contains: supplier/buyer details, item description, quantity, price excluding tax, tax, total amount.

### 1.2 Benefits
- Unified invoicing process; automation reduces manual efforts and errors.
- Facilitates tax return filing and system integration.
- For larger businesses: streamlined operations, cost savings.
- For MSMEs: phased implementation, progressive transition.

### 1.3 Transaction Types
- B2B, B2C, B2G (B2G flow similar to B2B).
- Applies to all persons in Malaysia including: Association, Body of persons, Branch, Business trust, Co-operative societies, Corporations, LLP, Partnership, Property trust fund, Real estate investment trust, Representative/regional office, Trust body, Unit trust.

### 1.4 Scenarios and Types

**Scenarios requiring e-Invoice:**
1. Proof of Income: sale or transaction to recognise income.
2. Proof of Expense: purchases, spending, returns, discounts; or self-billed e-Invoice for foreign supplier transactions (when foreign supplier does not use MyInvois).

**Types of e-Invoices:**
1. **Invoice**: Commercial document between Supplier and Buyer; includes self-billed e-Invoice for expense.
2. **Credit Note**: Issued by Supplier to correct errors, apply discounts, or account for returns; reduces value of original e-Invoice; no return of monies to Buyer.
3. **Debit Note**: Indicates additional charges on a previously issued e-Invoice.
4. **Refund Note**: Issued by Supplier to confirm refund of Buyer's payment (return of monies).

### 1.5 Implementation Timeline (Table 1.1)

| No. | Targeted Taxpayers (annual turnover/revenue) | Implementation Date |
|-----|---------------------------------------------|---------------------|
| 1 | More than RM100 million | 1 August 2024 |
| 2 | More than RM25 million and up to RM100 million | 1 January 2025 |
| 3 | More than RM5 million and up to RM25 million | 1 July 2025 |
| 4 | Up to RM5 million | 1 January 2026 |

**Determination of turnover/revenue:**
- With audited financial statements: Based on statement of comprehensive income for FY2022.
- Without audited financial statements: Based on annual revenue in tax return for YA 2022.
- Change of accounting year end: turnover pro-rated to 12-month period.

Compliance obligation is from issuance perspective. Invoices issued prior to implementation date are not required to be converted. New businesses (2023-2025) with turnover ≥ RM1,000,000: 1 July 2026. New businesses from 2026: 1 July 2026 or operation commencement date; if first year turnover < RM1,000,000, then 1 January in second year after turnover reached RM1,000,000.

### 1.6 Exemptions

**Exempt from issuing e-Invoice (1.6.1):**
(a) Foreign diplomatic office
(b) Individual not conducting business
(c) Statutory body/authority/local authority – for collection of payment/fee/charge/levy/summon/compound/penalty under written law; and for goods/services before 1 July 2025
(d) International organisation – for goods/services before 1 July 2025
(e) Taxpayers with annual turnover/revenue less than RM1,000,000

Suppliers who provide to above persons still must issue e-Invoice per timeline. Entities owned by exempt persons still must implement e-Invoice.

**Not required (1.6.7):** Employment income; Pension; Alimony; Dividend (specific circumstances); Zakat; Contract value for buying/selling securities or derivatives on exchange; Disposal of shares (unlisted, except where disposer is company/LLP/trust body/co-operative); Donations/contributions as per FAQ.

---

## 2.0 GETTING READY FOR E-INVOICE

### 2.2 Two mechanisms
1. **MyInvois Portal**: Individual form or batch upload via Excel. Accessible to all; for those without API.
2. **API**: High-volume; ERP integration, Peppol, or non-Peppol providers. Requires tech investment.

### 2.3 MyInvois Portal workflow
- Login via MyTax Portal (https://mytax.hasil.gov.my).
- TIN: retrieve/verify via MyTax Portal or e-Daftar.
- Step 1: Create and submit (individual form or batch Excel).
- Step 2: Validation (near real-time); receive validated e-Invoice + PDF with IRBM Unique Identifier, date/time, validation link.
- Step 3: Notification to Supplier and Buyer (email).
- Step 4: Supplier must share validated e-Invoice or visual representation (with QR code) to Buyer.
- Step 5–7: Buyer can request rejection within 72 hours; Supplier can cancel within 72 hours. After 72 hours, use credit/debit/refund note.
- Step 8: Validated e-Invoices stored in IRBM database; taxpayers must retain records.
- Step 9: Request/retrieve via Portal in XML/JSON, Metadata, Grid, PDF.

### 2.4 API workflow
- Formats: XML or JSON (UBL2.1 structure).
- 55 required data fields in 8 categories: Address, Business Details, Contact Number, Invoice Details, Parties, Party Details, Payment Info, Products/Services.
- Digital certificate (.cer or .pfx) required for API; digital signature in submission.
- Steps parallel to Portal: Submit → Validate → Share (with QR in visual) → Rejection/Cancellation within 72h → Store → Reporting via API (XML/JSON, Metadata).

### 2.5 Validation
- Statuses: Submitted (passed structure/core); Valid (all checks); Invalid (failed); Cancelled (by Supplier within 72h).
- Validators: Structure, Core Fields, Signature (background), Taxpayer (background), Referenced Documents (background), Code, Duplicate Document (background).
- System disruption: DG IR evaluates case-by-case; evidence of compliance efforts may avoid action.

### 2.6 IRBM shares e-Invoice info with RMCD (Section 138(4)(aa) ITA 1967).

---

## APPENDIX 1 – REQUIRED FIELDS (summary)

Parties: Supplier's Name, Buyer's Name.
Supplier: TIN, Registration/ID/Passport, SST No. (if SST), Tourism Tax No. (if applicable), Email (optional), MSIC Code, Business activity description.
Buyer: TIN, Registration/ID/Passport, SST No. (if SST), Email (optional).
Address: Supplier's Address, Buyer's Address.
Contact: Supplier's Contact Number, Buyer's Contact Number.
Invoice details: Version, Type, Code/Number, Original e-Invoice Reference (for CN/DN/Refund), Date and Time, Issuer's Digital Signature, Currency Code, Exchange Rate (if applicable), Billing Frequency/Period (optional).
Products/Services: Classification, Description, Unit Price, Tax Type, Tax Rate (if applicable), Tax Amount, Tax Exemption details/amount (if applicable), Subtotal, Total Excluding Tax, Total Including Tax, Total Net (optional), Total Payable, Rounding (optional), Quantity/Measurement (optional), Discount/Fee (optional).
Payment: Payment Mode, Supplier's Bank Account, Payment Terms, Prepayment amount/date/reference, Bill Reference (optional).

---

## APPENDIX 2 – ANNEXURE

Import/export: Reference Number of Customs Form No.1, 9 (mandatory where applicable).
Shipping to different recipient (optional): Shipping recipient name, address, TIN, Registration/ID/Passport.
Import/export optional: Incoterms, Product Tariff Code, FTA info (export), Certified Exporter number (export), Customs Form No.2, Country of Origin, Other charges.

---

## APPENDIX 3 – INTERNATIONAL ORGANISATIONS (exempt pre-1 July 2025)

Include: ADB, ASEAN, ICRC, IFRC, ILO, IsDB, UNICEF, UNDP, UNESCO, WHO, World Bank Group, WFP, etc. (full list in guideline).

---

## GLOSSARY (abbreviations)

API, B2B, B2C, B2G, ERP, FTA, IRBM, JSON, MSIC, MSME, SDK, SSM, SST, TIN, UBL2.1, XML.

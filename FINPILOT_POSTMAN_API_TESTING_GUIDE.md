# FinPilot AI — Complete Postman API Testing Guide

> **For beginners.** Read this top to bottom before opening Postman. Every API is explained with what it needs, what it returns, and what order to run it in.

---

## Table of Contents

1. [How FinPilot Auth Works](#1-how-finpilot-auth-works)
2. [Files to Import into Postman](#2-files-to-import-into-postman)
3. [Postman Setup Checklist](#3-postman-setup-checklist)
4. [Environment Variables Reference](#4-environment-variables-reference)
5. [Complete API Inventory](#5-complete-api-inventory)
6. [API Dependency Map](#6-api-dependency-map)
7. [Correct Execution Sequence (All 70 APIs)](#7-correct-execution-sequence-all-70-apis)
8. [Phase-by-Phase Guide](#8-phase-by-phase-guide)
9. [Postman Test Scripts](#9-postman-test-scripts)
10. [Error Troubleshooting Guide](#10-error-troubleshooting-guide)
11. [Golden Rules Quick Reference](#11-golden-rules-quick-reference)

---

## 1. How FinPilot Auth Works

Before you send a single request, understand these 3 concepts. They are different from most APIs.

### A. No JWT Token — Cookie-Based Sessions

FinPilot does **NOT** use `Authorization: Bearer <token>` headers.

Instead, Django uses **browser-style cookies**:
- After login, Django sets a `sessionid` cookie in your browser/Postman.
- Postman automatically sends this cookie with every future request (if cookie management is ON).
- You do NOT need to copy any token manually.

### B. CSRF Token — Required for Every Write Request

Any request that **changes data** (POST, PUT, PATCH) needs a special security token called a **CSRF token**.

- You get it by calling `GET /api/v1/auth/csrf/` first.
- It arrives as a cookie called `csrftoken`.
- You must include it as a **header**: `X-CSRFToken: {{csrf_token}}`
- The test script in the collection captures it automatically into `{{csrf_token}}`.

### C. Organization ID — Required for All Business Data

Every API that deals with business data (customers, invoices, payments, etc.) needs to know **which organization** you are working with.

- After login, run `GET /api/v1/auth/me/` — the test script saves your org ID into `{{organization_id}}`.
- Include it as a header on every org-scoped request: `X-Organization-ID: {{organization_id}}`

### Summary Table

| What you need | Where you get it | How you send it |
|---|---|---|
| Session (login) | `POST /auth/login/` → `sessionid` cookie | Postman sends automatically |
| CSRF Token | `GET /auth/csrf/` → `csrftoken` cookie | Header: `X-CSRFToken: {{csrf_token}}` |
| Organization ID | `GET /auth/me/` → `organizations[0].id` | Header: `X-Organization-ID: {{organization_id}}` |

---

## 2. Files to Import into Postman

You have **1 collection file** and **1 environment file** in your `postman/` folder:

| File | Purpose |
|---|---|
| `FinPilot_Collection.json` | Contains all 70 API requests organized in 19 folders |
| `FinPilot_Environment.json` | Contains all variables (`base_url`, `csrf_token`, `organization_id`, etc.) |

### How to Import

1. Open Postman
2. Click **Import** (top left)
3. Drag both JSON files in (or click "Upload Files" and select both)
4. You will see a new collection: **"FinPilot AI - Complete API Collection"**
5. You will see a new environment: **"FinPilot AI - Local Dev"**
6. Click the **environment dropdown** (top right) → Select **"FinPilot AI - Local Dev"**

> **Note:** There is only ONE collection file (not two as mentioned in the request). The guide covers every API in it.

---

## 3. Postman Setup Checklist

Do these **before** running any request:

- [ ] Import `FinPilot_Collection.json`
- [ ] Import `FinPilot_Environment.json`
- [ ] Select **"FinPilot AI - Local Dev"** environment (top-right dropdown)
- [ ] Go to **Settings → General** → Turn ON **"Automatically follow redirects"**
- [ ] Go to **Settings → General** → Ensure **Cookie management** is ON (it is by default)
- [ ] Make sure your backend is running: `http://127.0.0.1:8000`
- [ ] Make sure PostgreSQL and Redis are running (Docker containers or native)

---

## 4. Environment Variables Reference

### Variables Already in the Environment File

| Variable | Default Value | Description | Auto-captured? |
|---|---|---|---|
| `base_url` | `http://127.0.0.1:8000` | Django backend URL | No — set manually if deploying |
| `organization_id` | _(empty)_ | Your org's UUID | ✅ Yes — by "Get Current User (me)" |
| `csrf_token` | _(empty)_ | CSRF security token | ✅ Yes — by "Get CSRF Token" |
| `test_customer_id` | _(empty)_ | UUID of a created customer | ✅ Yes — by "Create Customer" |
| `test_invoice_id` | _(empty)_ | UUID of a created invoice | ✅ Yes — by "Create Invoice" |
| `test_payment_id` | _(empty)_ | UUID of a created payment | ✅ Yes — by "Record Payment" |
| `test_product_id` | _(empty)_ | UUID of a created product | ✅ Yes — by "Create Product" |
| `test_gst_rate_id` | _(empty)_ | UUID of a GST rate | ✅ Yes — by "List GST Rates" or "Create GST Rate" |
| `test_import_batch_id` | _(empty)_ | UUID of an invoice import batch | ✅ Yes — by "Upload Invoice File" |
| `test_bank_batch_id` | _(empty)_ | UUID of a bank statement import | ✅ Yes — by "Upload Bank Statement" |
| `test_recon_match_id` | _(empty)_ | UUID of a reconciliation match | ✅ Yes — by "List Reconciliation Matches" |
| `test_notification_id` | _(empty)_ | UUID of a notification | ✅ Yes — by "List Notifications" |
| `test_reminder_template_id` | _(empty)_ | UUID of a reminder template | ✅ Yes — by "Create Template" |
| `test_reminder_policy_id` | _(empty)_ | UUID of a reminder policy | ✅ Yes — by "Create Policy" |
| `test_reminder_job_id` | _(empty)_ | UUID of a reminder job | ✅ Yes — by "List Reminder Jobs" |
| `test_allocation_id` | _(empty)_ | UUID of a payment allocation | ✅ Yes — by "Record Payment" |

### Variables NOT in the Environment (Missing — Add These)

| Variable | Why you need it | How to add |
|---|---|---|
| `test_user_email` | Store your login email for reference | Add manually |
| `test_invoice_id_2` | If you create multiple invoices | Add manually after test |

> **How to add a missing variable:** In Postman, click the environment name → "Edit" → scroll down → click "Add a new row"

---

## 5. Complete API Inventory

**Total: 70 APIs across 19 folders**

| Folder | APIs | Count |
|---|---|---|
| 01 - Authentication | CSRF, Register, Login, Get Me, Logout | 5 |
| 02 - Organizations | List, Create, Get Detail, Update (PATCH), List Members | 5 |
| 03 - Dashboard & Reports | Dashboard, Aging (Today), Aging (Custom Date) | 3 |
| 04 - Customers | List, Create, Get Detail, Update (PATCH), Full Update (PUT), Opt-Out, Opt-In | 7 |
| 05 - GST Rates | List, Create, Get Detail, Update (PATCH), Deactivate, Activate | 6 |
| 06 - Products | List, Create, Get Detail, Update (PATCH), Deactivate, Activate | 6 |
| 07 - Invoices | List, Create (with GST items), Create (header-only), Get Detail, Update (PUT), Void | 6 |
| 08 - Payments | List, Record (with allocation), Record (no allocation), Get Detail, Reverse Allocation | 5 |
| 09 - AI Assistant | Ask Question, Ask Top Overdue, Ask Cash Flow, Validation Error Test | 4 |
| 10 - Notifications | List, Mark Single Read, Mark All Read | 3 |
| 11 - Forecast | 30-day (due date), 7-day (historical), 60-day (custom offset) | 3 |
| 12 - Reminders / Templates | List, Create, Get Detail, Update (PATCH), Approve Revision | 5 |
| 12 - Reminders / Policies | List, Create, Get Detail, Activate Auto, Deactivate Auto | 5 |
| 12 - Reminders / Jobs | List, Get Detail, Approve, Reject | 4 |
| 13 - Reconciliation | Upload Bank Statement, Confirm Mapping, List Matches, Confirm Match, Reject Match | 5 |
| 14 - Invoice Imports | Download CSV Template, Download XLSX Template, Upload File, Get Batch Status, Commit | 5 |
| 15 - Exports | Export Invoices (CSV), Export Customers (CSV), Export Payments (CSV) | 3 |
| 16 - Audit Log | List Audit Logs | 1 |
| 17 - Subscriptions | Get Subscription Status | 1 |
| 18 - Platform Admin | List All Orgs, List All Users, Platform Audit Log | 3 |
| 19 - OpenAPI Schema | Schema (JSON), Swagger UI | 2 |

---

## 6. API Dependency Map

This diagram shows what each API needs before it can work:

```
[No dependencies — run first]
  └── GET  /auth/csrf/              ← Must be FIRST
  └── GET  /api/schema/             ← Independent
  └── GET  /api/schema/swagger-ui/  ← Independent

[Needs: CSRF token only]
  └── POST /auth/register/          ← Creates user + org

[Needs: CSRF token + existing account]
  └── POST /auth/login/             ← Creates session

[Needs: active session]
  └── GET  /auth/me/                ← Gets & saves organization_id
  └── POST /auth/logout/

[Needs: session + organization_id]
  └── GET  /organizations/
  └── POST /organizations/          ← Can create extra orgs
  └── GET  /organizations/{id}/
  └── PATCH /organizations/{id}/
  └── GET  /members/
  └── GET  /dashboard/
  └── GET  /reports/aging/
  └── GET  /notifications/
  └── GET  /subscriptions/
  └── GET  /audit-logs/
  └── GET  /exports/invoices/
  └── GET  /exports/customers/
  └── GET  /exports/payments/
  └── GET  /forecasts/
  └── GET  /imports/invoice-template/csv/
  └── GET  /imports/invoice-template/xlsx/

[Needs: session + org + CSRF]
  └── POST /gst-rates/              → saves test_gst_rate_id
  └── POST /customers/              → saves test_customer_id

[Needs: test_gst_rate_id]
  └── POST /products/               → saves test_product_id

[Needs: test_customer_id]
  └── POST /invoices/               → saves test_invoice_id

[Needs: test_customer_id + test_invoice_id]
  └── POST /payments/ (with allocation) → saves test_payment_id + test_allocation_id

[Needs: test_payment_id + test_allocation_id]
  └── POST /payments/{id}/allocations/{id}/reverse/

[Needs: test_reminder_template_id]
  └── POST /reminders/policies/     → saves test_reminder_policy_id

[Needs: test_reminder_policy_id + invoices exist]
  └── GET  /reminders/jobs/         → saves test_reminder_job_id

[Needs: bank statement uploaded → test_bank_batch_id]
  └── POST /imports/bank-statements/{id}/confirm-mapping/
  └── GET  /reconciliation/         → saves test_recon_match_id

[Needs: test_recon_match_id]
  └── POST /reconciliation/{id}/confirm/
  └── POST /reconciliation/{id}/reject/

[Needs: test_import_batch_id]
  └── GET  /imports/invoices/{id}/
  └── POST /imports/invoices/{id}/commit/

[Superuser session required]
  └── GET  /admin/orgs/
  └── GET  /admin/users/
  └── GET  /admin/audit-logs/
```

---

## 7. Correct Execution Sequence (All 70 APIs)

**Legend:**
- 🔴 **MANDATORY** — must run; nothing else works without it
- 🟡 **RECOMMENDED** — run to set up environment variables  
- 🟢 **OPTIONAL** — test a specific feature, can skip
- 🔵 **INDEPENDENT** — no prerequisites, can run anytime (after login)
- ⚠️ **DESTRUCTIVE** — changes or deletes data; run carefully

---

### STEP 0 — Before anything else (No auth needed)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 0a | OpenAPI Schema | GET | `/api/schema/` | 🔵 Independent |
| 0b | Swagger UI | GET | `/api/schema/swagger-ui/` | 🔵 Independent |

---

### PHASE 1 — Authentication (Run in this exact order)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 1 | **Get CSRF Token** | GET | `/api/v1/auth/csrf/` | 🔴 MANDATORY |
| 2 | Register New User | POST | `/api/v1/auth/register/` | 🟡 (skip if account exists) |
| 3 | **Login** | POST | `/api/v1/auth/login/` | 🔴 MANDATORY |
| 4 | **Get Current User (me)** | GET | `/api/v1/auth/me/` | 🔴 MANDATORY (sets org ID) |
| *(end)* | Logout | POST | `/api/v1/auth/logout/` | 🟢 Run only when done testing |

> **Why this order?**
> - Step 1 must be first — CSRF token required for step 2 and 3.
> - Step 2 is optional if you already have a test account (use `test@finpilot.local` / `Test@1234`).
> - Step 4 is mandatory — it sets `organization_id` which every other API needs.

---

### PHASE 2 — Organization Setup

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 5 | List My Organizations | GET | `/api/v1/organizations/` | 🟡 Verify org exists |
| 6 | Get Organization Detail | GET | `/api/v1/organizations/{{organization_id}}/` | 🟡 Check org settings |
| 7 | Update Organization (PATCH) | PATCH | `/api/v1/organizations/{{organization_id}}/` | 🟢 Optional |
| 8 | List Team Members | GET | `/api/v1/members/` | 🟢 Optional |
| 9 | Create Organization | POST | `/api/v1/organizations/` | 🟢 Only if you want a second org |

---

### PHASE 3 — Read-Only Checks (Safe to run anytime after login)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 10 | Get Dashboard | GET | `/api/v1/dashboard/` | 🔵 Independent |
| 11 | Aging Report (Today) | GET | `/api/v1/reports/aging/` | 🔵 Independent |
| 12 | Aging Report (Custom Date) | GET | `/api/v1/reports/aging/?as_of=2026-10-31` | 🔵 Independent |
| 13 | Get Subscription Status | GET | `/api/v1/subscriptions/` | 🔵 Independent |
| 14 | List Notifications | GET | `/api/v1/notifications/` | 🔵 Independent (saves notification_id) |

---

### PHASE 4 — Business Data Setup (Run in order)

#### 4A — GST Rates (Must come before Products and Invoices)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 15 | **List GST Rates** | GET | `/api/v1/gst-rates/?page_size=200` | 🔴 MANDATORY (auto-saves gst_rate_id) |
| 16 | Create GST Rate | POST | `/api/v1/gst-rates/` | 🟢 Only if list is empty |
| 17 | Get GST Rate Detail | GET | `/api/v1/gst-rates/{{test_gst_rate_id}}/` | 🟢 Optional |
| 18 | Update GST Rate (PATCH) | PATCH | `/api/v1/gst-rates/{{test_gst_rate_id}}/` | 🟢 Optional |
| 19 | Deactivate GST Rate | POST | `/api/v1/gst-rates/{{test_gst_rate_id}}/deactivate/` | ⚠️ Optional |
| 20 | Activate GST Rate | POST | `/api/v1/gst-rates/{{test_gst_rate_id}}/activate/` | 🟢 Undo step 19 |

> **Important:** Registration auto-seeds default GST rates (5%, 12%, 18%, 28%). Just run "List GST Rates" and the script saves the first one automatically. You may not need to create any.

#### 4B — Customers (Must come before Invoices and Payments)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 21 | List Customers | GET | `/api/v1/customers/?page_size=25` | 🟡 Check existing customers |
| 22 | **Create Customer** | POST | `/api/v1/customers/` | 🔴 MANDATORY (saves customer_id) |
| 23 | Get Customer Detail | GET | `/api/v1/customers/{{test_customer_id}}/` | 🟢 Optional |
| 24 | Update Customer (PATCH) | PATCH | `/api/v1/customers/{{test_customer_id}}/` | 🟢 Optional |
| 25 | Full Update Customer (PUT) | PUT | `/api/v1/customers/{{test_customer_id}}/` | 🟢 Optional |
| 26 | Customer Opt-Out | POST | `/api/v1/customers/{{test_customer_id}}/opt-out/` | 🟢 Optional |
| 27 | Customer Opt-In | POST | `/api/v1/customers/{{test_customer_id}}/opt-in/` | 🟢 Undo step 26 |

#### 4C — Products (Optional; needs GST rate ID)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 28 | List Products | GET | `/api/v1/products/?page_size=200` | 🟢 Optional |
| 29 | Create Product | POST | `/api/v1/products/` | 🟢 Optional (saves product_id) |
| 30 | Get Product Detail | GET | `/api/v1/products/{{test_product_id}}/` | 🟢 Optional |
| 31 | Update Product (PATCH) | PATCH | `/api/v1/products/{{test_product_id}}/` | 🟢 Optional |
| 32 | Deactivate Product | POST | `/api/v1/products/{{test_product_id}}/deactivate/` | ⚠️ Optional |
| 33 | Activate Product | POST | `/api/v1/products/{{test_product_id}}/activate/` | 🟢 Undo step 32 |

---

### PHASE 5 — Financial Operations (Run in order)

#### 5A — Invoices (Needs: customer_id)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 34 | List Invoices | GET | `/api/v1/invoices/?page_size=25` | 🟡 Check existing invoices |
| 35 | **Create Invoice (with GST items)** | POST | `/api/v1/invoices/` | 🔴 MANDATORY (saves invoice_id) |
| 36 | Create Invoice (header-only) | POST | `/api/v1/invoices/` | 🟢 Alternative format |
| 37 | Get Invoice Detail | GET | `/api/v1/invoices/{{test_invoice_id}}/` | 🟡 Verify GST calculation |
| 38 | Update Invoice (PUT) | PUT | `/api/v1/invoices/{{test_invoice_id}}/` | 🟢 Optional (before payment) |
| 39 | Void Invoice | POST | `/api/v1/invoices/{{test_invoice_id}}/void/` | ⚠️ Run LAST in this group |

#### 5B — Payments (Needs: customer_id + invoice_id)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 40 | List Payments | GET | `/api/v1/payments/?page_size=25` | 🟡 Check existing payments |
| 41 | **Record Payment (with allocation)** | POST | `/api/v1/payments/` | 🔴 MANDATORY (saves payment_id + allocation_id) |
| 42 | Record Payment (no allocation) | POST | `/api/v1/payments/` | 🟢 Optional |
| 43 | Get Payment Detail | GET | `/api/v1/payments/{{test_payment_id}}/` | 🟡 Verify allocation |
| 44 | Reverse Payment Allocation | POST | `/api/v1/payments/{{test_payment_id}}/allocations/{{test_allocation_id}}/reverse/` | ⚠️ Optional, destructive |

---

### PHASE 6 — Advanced Features

#### 6A — AI Assistant (Needs: session + org + data)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 45 | Ask a Question | POST | `/api/v1/assistant/` | 🟢 Needs OPENAI_API_KEY in .env |
| 46 | Ask About Top Overdue | POST | `/api/v1/assistant/` | 🟢 Optional |
| 47 | Ask About Cash Flow | POST | `/api/v1/assistant/` | 🟢 Optional |
| 48 | Validation Error Test | POST | `/api/v1/assistant/` | 🟢 Expects 400 error |

> **Note:** Returns 503 if `OPENAI_API_KEY` is not set in `backend/.env`.

#### 6B — Forecasts (Needs: invoices to exist)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 49 | Forecast (30 days, due date) | GET | `/api/v1/forecasts/?period=30&timing=due_date` | 🟢 Optional |
| 50 | Forecast (7 days, historical) | GET | `/api/v1/forecasts/?period=7&timing=historical_delay` | 🟢 Optional |
| 51 | Forecast (60 days, custom offset) | GET | `/api/v1/forecasts/?period=60&timing=custom_offset&offset=7` | 🟢 Optional |

#### 6C — Reminders (Needs: template before policy; policy before jobs)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 52 | List Templates | GET | `/api/v1/reminders/templates/` | 🟡 Check existing |
| 53 | Create Template | POST | `/api/v1/reminders/templates/` | 🟡 Saves template_id |
| 54 | Get Template Detail | GET | `/api/v1/reminders/templates/{{test_reminder_template_id}}/` | 🟢 |
| 55 | Update Template (PATCH) | PATCH | `/api/v1/reminders/templates/{{test_reminder_template_id}}/` | 🟢 |
| 56 | Approve Template Revision | POST | `/api/v1/reminders/templates/{{test_reminder_template_id}}/approve-revision/` | 🟢 After PATCH |
| 57 | List Policies | GET | `/api/v1/reminders/policies/` | 🟡 Check existing |
| 58 | Create Policy | POST | `/api/v1/reminders/policies/` | 🟡 Needs template_id; saves policy_id |
| 59 | Get Policy Detail | GET | `/api/v1/reminders/policies/{{test_reminder_policy_id}}/` | 🟢 |
| 60 | Activate Auto-Send | POST | `/api/v1/reminders/policies/{{test_reminder_policy_id}}/activate-auto/` | ⚠️ Optional |
| 61 | Deactivate Auto-Send | POST | `/api/v1/reminders/policies/{{test_reminder_policy_id}}/deactivate-auto/` | 🟢 Undo step 60 |
| 62 | List Reminder Jobs | GET | `/api/v1/reminders/jobs/` | 🟡 Saves job_id (if any exist) |
| 63 | Get Reminder Job Detail | GET | `/api/v1/reminders/jobs/{{test_reminder_job_id}}/` | 🟢 |
| 64 | Approve Reminder Job | POST | `/api/v1/reminders/jobs/{{test_reminder_job_id}}/approve/` | 🟢 |
| 65 | Reject Reminder Job | POST | `/api/v1/reminders/jobs/{{test_reminder_job_id}}/reject/` | 🟢 |

#### 6D — Reconciliation (Needs: invoices + payments + bank statement)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 66 | Upload Bank Statement | POST | `/api/v1/imports/bank-statements/` | 🟡 Saves bank_batch_id |
| 67 | Confirm Column Mapping | POST | `/api/v1/imports/bank-statements/{{test_bank_batch_id}}/confirm-mapping/` | 🟡 After step 66 |
| 68 | List Reconciliation Matches | GET | `/api/v1/reconciliation/` | 🟡 Saves recon_match_id |
| 69 | Confirm Match | POST | `/api/v1/reconciliation/{{test_recon_match_id}}/confirm/` | ⚠️ Creates payment automatically |
| 70 | Reject Match | POST | `/api/v1/reconciliation/{{test_recon_match_id}}/reject/` | 🟢 Alternative to confirm |

#### 6E — Invoice Imports (Bulk upload)

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 71 | Download CSV Template | GET | `/api/v1/imports/invoice-template/csv/` | 🟡 Get the template first |
| 72 | Download XLSX Template | GET | `/api/v1/imports/invoice-template/xlsx/` | 🟢 Alternative |
| 73 | Upload Invoice File | POST | `/api/v1/imports/invoices/` | 🟡 Saves import_batch_id |
| 74 | Get Batch Status & Preview | GET | `/api/v1/imports/invoices/{{test_import_batch_id}}/` | 🟡 Review before commit |
| 75 | Commit Import Batch | POST | `/api/v1/imports/invoices/{{test_import_batch_id}}/commit/` | ⚠️ Creates invoices |

---

### PHASE 7 — Exports and Audit

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 76 | Export Invoices (CSV) | GET | `/api/v1/exports/invoices/` | 🔵 Independent |
| 77 | Export Customers (CSV) | GET | `/api/v1/exports/customers/` | 🔵 Independent |
| 78 | Export Payments (CSV) | GET | `/api/v1/exports/payments/` | 🔵 Independent |
| 79 | List Audit Logs | GET | `/api/v1/audit-logs/` | 🔵 Independent |

> **For exports:** Use **"Send and Download"** button in Postman (not just "Send") to save the CSV file.

---

### PHASE 8 — Notifications Management

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 80 | Mark Single Notification Read | POST | `/api/v1/notifications/{{test_notification_id}}/read/` | 🟢 After listing notifications |
| 81 | Mark All Notifications Read | POST | `/api/v1/notifications/mark-all-read/` | 🟢 Optional |

---

### PHASE 9 — Platform Admin (Superuser Only)

> Log in with `abhishekkumarsahu345@gmail.com` (superuser) for these.

| # | Name | Method | Endpoint | Type |
|---|---|---|---|---|
| 82 | List All Organizations | GET | `/api/v1/admin/orgs/` | 🟢 Superuser only |
| 83 | List All Users | GET | `/api/v1/admin/users/` | 🟢 Superuser only |
| 84 | Platform-Wide Audit Log | GET | `/api/v1/admin/audit-logs/` | 🟢 Superuser only |

---

## 8. Phase-by-Phase Guide

### Phase 1 — Authentication (Detailed Steps)

#### API 1: Get CSRF Token
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/auth/csrf/`
- **Headers:** None
- **Body:** None
- **Auth required:** No
- **CSRF required:** No
- **What happens:** Sets a cookie called `csrftoken` in Postman
- **What to save:** The test script automatically saves it to `{{csrf_token}}`
- **Expected response:** `200 OK` with body `{"detail": "CSRF cookie set"}`

#### API 2: Register New User (Optional if account exists)
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/register/`
- **Headers:**
  ```
  Content-Type: application/json
  X-CSRFToken: {{csrf_token}}
  ```
- **Body:**
  ```json
  {
    "full_name": "Rahul Sharma",
    "email": "rahul@acme.com",
    "password": "SecurePass@123",
    "organization_name": "Acme Industries Pvt Ltd"
  }
  ```
- **Auth required:** No
- **CSRF required:** Yes
- **What happens:** Creates user + creates organization + seeds default GST rates (0%, 5%, 12%, 18%, 28%)
- **What to save:** Test script saves `organization_id` from `body.organization_id`
- **Expected response:** `201 Created`
- **⚠️ Skip this if** you already have an account — use the test accounts from README instead

#### API 3: Login
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/auth/login/`
- **Headers:**
  ```
  Content-Type: application/json
  X-CSRFToken: {{csrf_token}}
  ```
- **Body:**
  ```json
  {
    "username": "test@finpilot.local",
    "password": "Test@1234"
  }
  ```
  > **Note:** The field is named `username` but it accepts an email address.
- **Auth required:** No
- **CSRF required:** Yes
- **What happens:** Sets `sessionid` cookie
- **Expected response:** `200 OK` with `{"detail": "Signed in"}`
- **If you get 400:** Check username/password. Field must be `username`, not `email`.

#### API 4: Get Current User (me) — CRITICAL
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/auth/me/`
- **Headers:** None
- **Auth required:** Yes (session cookie)
- **CSRF required:** No
- **What happens:** Returns user info and organization list; test script saves org ID
- **What to save:** Test script automatically saves `body.organizations[0].id` → `{{organization_id}}`
- **Expected response:**
  ```json
  {
    "id": "uuid...",
    "email": "test@finpilot.local",
    "full_name": "Test User",
    "organizations": [
      {
        "id": "uuid...",
        "name": "...",
        "role": "member"
      }
    ]
  }
  ```

---

### Phase 4B — Creating a Customer (Detailed)

#### API 22: Create Customer
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/customers/`
- **Headers:**
  ```
  Content-Type: application/json
  X-CSRFToken: {{csrf_token}}
  X-Organization-ID: {{organization_id}}
  ```
- **Body:**
  ```json
  {
    "name": "XYZ Technologies Pvt Ltd",
    "contact_name": "Priya Mehta",
    "email": "priya@xyztechnologies.com",
    "phone": "9876543210",
    "billing_address": "Plot 42, MIDC, Pune - 411001",
    "gstin": "27AABCX1234A1Z5",
    "state": "Maharashtra",
    "payment_terms_days": 30,
    "notes": "Key client"
  }
  ```
  > **Only `name` is required.** All other fields are optional.
- **GSTIN format:** 15 characters — `22AAAAA0000A1Z5` (state code + PAN + entity number + check digit)
- **Expected response:** `201 Created` with the customer's `id`
- **What to save:** Test script saves `body.id` → `{{test_customer_id}}`

---

### Phase 5A — Creating an Invoice (Detailed)

#### API 35: Create Invoice (with GST line items)
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/invoices/`
- **Headers:**
  ```
  Content-Type: application/json
  X-CSRFToken: {{csrf_token}}
  X-Organization-ID: {{organization_id}}
  ```
- **Body:**
  ```json
  {
    "customer": "{{test_customer_id}}",
    "invoice_number": "INV-2026-001",
    "invoice_date": "2026-11-01",
    "due_date": "2026-11-30",
    "currency": "INR",
    "discount_minor": 0,
    "notes": "Q4 consulting services",
    "status": "issued",
    "items": [
      {
        "product": null,
        "description": "IT Consulting — 10 hours",
        "quantity": 10,
        "unit_price_minor": 500000,
        "discount_minor": 0,
        "gst_rate_bps": 1800,
        "gst_rate_name": "GST 18%",
        "hsn_sac": "9983",
        "sort_order": 0
      }
    ]
  }
  ```
- **Money encoding:**
  - All amounts are in **PAISE** (Indian minor unit)
  - ₹1 = 100 paise
  - ₹5,000 = `500000`
  - ₹1,00,000 = `10000000`
- **GST encoding:**
  - `gst_rate_bps` is in basis points
  - 100 bps = 1%
  - 18% GST = `1800`
  - 5% GST = `500`
  - 28% GST = `2800`
- **Server auto-calculates:** subtotal, tax, total (you don't need to send these)
- **Expected response:** `201 Created` with the invoice's `id` and `total_minor`
- **What to save:** Test script saves `body.id` → `{{test_invoice_id}}`

---

### Phase 5B — Recording a Payment (Detailed)

#### API 41: Record Payment (with allocation)
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/payments/`
- **Headers:**
  ```
  Content-Type: application/json
  X-CSRFToken: {{csrf_token}}
  X-Organization-ID: {{organization_id}}
  ```
- **Body:**
  ```json
  {
    "customer": "{{test_customer_id}}",
    "payment_date": "2026-11-10",
    "amount_minor": 500000,
    "currency": "INR",
    "method": "upi",
    "reference": "UPI-TXN-9876543210",
    "notes": "Payment for INV-2026-001",
    "allocations_input": [
      {
        "invoice": "{{test_invoice_id}}",
        "amount_minor": 500000
      }
    ]
  }
  ```
- **Payment method options:** `bank_transfer`, `upi`, `cheque`, `cash`, `card`, `other`
- **Allocation rule:** The allocation `amount_minor` cannot exceed the invoice's outstanding balance
- **Expected response:** `201 Created` with `id`, `allocations[]`, `unallocated_minor`
- **What to save:** Test script saves `body.id` → `{{test_payment_id}}` and `body.allocations[0].id` → `{{test_allocation_id}}`

---

## 9. Postman Test Scripts

The collection already has test scripts built in. Here is what each key script does and where to find it:

### Script: Capture CSRF Token (in "Get CSRF Token")
```javascript
pm.test('Status is 200', () => pm.response.to.have.status(200));
const cookie = pm.cookies.get('csrftoken');
if (cookie) {
    pm.environment.set('csrf_token', cookie);
    console.log('CSRF token captured: ' + cookie);
} else {
    console.warn('csrftoken cookie not found — check Postman cookie settings');
}
```

### Script: Capture Organization ID (in "Get Current User (me)")
```javascript
pm.test('Status is 200', () => pm.response.to.have.status(200));
const body = pm.response.json();
pm.test('Has organizations', () => pm.expect(body.organizations).to.be.an('array').with.length.above(0));
if (body.organizations && body.organizations.length > 0) {
    const orgId = body.organizations[0].id;
    pm.environment.set('organization_id', orgId);
    console.log('Organization ID auto-set: ' + orgId);
    console.log('Role: ' + body.organizations[0].role);
}
```

### Script: Capture Customer ID (in "Create Customer")
```javascript
pm.test('Status is 201', () => pm.response.to.have.status(201));
const body = pm.response.json();
if (body.id) {
    pm.environment.set('test_customer_id', body.id);
    console.log('Customer ID saved: ' + body.id);
}
```

### Script: Capture Invoice ID (in "Create Invoice")
```javascript
pm.test('Status is 201', () => pm.response.to.have.status(201));
const body = pm.response.json();
if (body.id) {
    pm.environment.set('test_invoice_id', body.id);
    console.log('Invoice ID saved: ' + body.id);
    console.log('Total: ' + body.total_minor + ' paise = ₹' + (body.total_minor/100));
}
```

### Script: Capture Payment ID + Allocation ID (in "Record Payment")
```javascript
pm.test('Status is 201', () => pm.response.to.have.status(201));
const body = pm.response.json();
if (body.id) {
    pm.environment.set('test_payment_id', body.id);
    if (body.allocations && body.allocations.length > 0) {
        pm.environment.set('test_allocation_id', body.allocations[0].id);
        console.log('Allocation ID saved: ' + body.allocations[0].id);
    }
}
```

### Script: Capture GST Rate ID (in "List GST Rates")
```javascript
pm.test('Status is 200', () => pm.response.to.have.status(200));
const body = pm.response.json();
if (body.results && body.results.length > 0) {
    pm.environment.set('test_gst_rate_id', body.results[0].id);
    console.log('First GST rate ID saved: ' + body.results[0].id);
}
```

> **Tip:** To view what a script captured, open **Postman Console** (View → Show Postman Console) before sending requests. All `console.log()` messages appear there.

---

## 10. Error Troubleshooting Guide

### 400 Bad Request

| Scenario | Cause | Fix |
|---|---|---|
| Login returns 400 | Wrong field name or wrong password | Use `username` field (not `email`), check password |
| Create Invoice returns 400 | Customer UUID is wrong or empty | Make sure `{{test_customer_id}}` is set (run Create Customer first) |
| Create Invoice returns 400 | Duplicate `invoice_number` | Change the number e.g. `INV-2026-002` |
| Void Invoice returns 400 | Invoice has active payment allocations | Reverse the allocation first |
| Update Invoice returns 400 | Trying to change total with active allocations | Reverse allocations first |
| Approve Policy Revision returns 400 | No pending revision | PATCH the template first to create a pending revision |
| Commit Batch returns 400 | Sending empty `row_ids` | Put the actual row UUIDs from batch detail response |
| AI Assistant returns 400 | Empty question field | The question must be 1–2000 characters |

### 401 Unauthorized

| Scenario | Cause | Fix |
|---|---|---|
| Any API after login | Session expired or not set | Re-run steps 1 → 3 → 4 (CSRF → Login → Me) |
| Got 401 immediately after login | Cookies not being sent | Check Postman Settings → turn on cookie management |

### 403 Forbidden

| Scenario | Cause | Fix |
|---|---|---|
| `/admin/orgs/`, `/admin/users/` | Not a superuser | Log in with `abhishekkumarsahu345@gmail.com` |
| Activate Policy Auto-Send | Need owner or manager role | Use an owner account |
| Approve Reminder Job | Need owner or manager role | Same as above |
| Update org fields | Need owner/manager/accountant role | Check your role in `GET /members/` |

### 404 Not Found

| Scenario | Cause | Fix |
|---|---|---|
| `/api/v1/customers/{{test_customer_id}}/` | Variable is empty | Run Create Customer first |
| `/api/v1/invoices/{{test_invoice_id}}/` | Variable is empty | Run Create Invoice first |
| Any `{{variable}}/` URL | UUID from another org | Make sure organization_id matches |

### 405 Method Not Allowed

| Scenario | Cause | Fix |
|---|---|---|
| Sent POST to a GET-only endpoint | Wrong HTTP method | Check the collection — use the method shown |

### 500 Internal Server Error

| Scenario | Cause | Fix |
|---|---|---|
| Any endpoint | Backend crashed | Check Django server terminal for the traceback |
| AI Assistant | Missing API key | Set `OPENAI_API_KEY` in `backend/.env` |
| Celery task failed | Redis not running | Check Redis is running on port 6379 |

### CSRF Token Errors (403 with "CSRF verification failed")

**Cause:** The `X-CSRFToken` header is missing or the token is stale.

**Fix:**
1. Re-run "Get CSRF Token" (GET `/api/v1/auth/csrf/`)
2. The test script updates `{{csrf_token}}` automatically
3. Make sure all POST/PUT/PATCH requests have the `X-CSRFToken: {{csrf_token}}` header

### "csrftoken cookie not found" Warning

**Cause:** Postman is not capturing cookies properly.

**Fix:**
1. Make sure you are NOT using Postman Interceptor mode
2. Go to Settings → General → ensure "Send cookies" is checked
3. If using the web version of Postman, switch to the desktop app

---

## 11. Golden Rules Quick Reference

| Rule | What it means |
|---|---|
| **CSRF first** | Always run "Get CSRF Token" before anything else |
| **Login second** | Run login right after CSRF token |
| **Me third** | Run "Get Current User" immediately after login — this sets org ID |
| **Money in paise** | ₹1 = 100. ₹5,000 = 500000. Never use decimals |
| **GST in bps** | 18% GST = 1800. Never use percentages directly |
| **X-Organization-ID required** | Every org-scoped API needs this header |
| **X-CSRFToken required** | Every POST, PUT, PATCH needs this header |
| **Watch the console** | Open Postman Console to see test script logs |
| **Register auto-seeds GST** | List GST Rates before creating them — they may already exist |
| **Don't void before checking** | Check if payment allocations exist before voiding an invoice |
| **Send and Download for exports** | CSV export endpoints return binary — use "Send and Download" |
| **503 from AI = no API key** | Set `OPENAI_API_KEY=sk-...` in `backend/.env` and restart Django |

---

## Appendix A — Test Accounts

| Email | Password | Role |
|---|---|---|
| `test@finpilot.local` | `Test@1234` | Member |
| `abhishekkumarsahu345@gmail.com` | *(reset if unknown)* | Superuser |
| `livetest99@example.com` | *(reset if unknown)* | Member |
| `apitest@finpilot.test` | *(reset if unknown)* | Member |

> To reset a password: open a terminal in the backend folder, activate `.venv`, and run:
> ```powershell
> python manage.py changepassword test@finpilot.local
> ```

---

## Appendix B — Important URLs

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000/api/v1/` | Base API URL |
| `http://127.0.0.1:8000/api/schema/swagger-ui/` | Interactive Swagger docs — browse all endpoints in browser |
| `http://127.0.0.1:8000/admin/` | Django admin panel |
| `http://localhost:5175/` | Frontend (React app) |

---

*Generated by analysis of `FinPilot_Collection.json`, `FinPilot_Environment.json`, and backend source code on 13 November 2026.*


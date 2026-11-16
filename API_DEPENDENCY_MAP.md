# FinPilot AI — API Dependency Map & Execution Architecture

> **Visual Architectural Dependency Reference.** Visualizes data flows, variable propagation handshakes, module hierarchies, and critical execution constraints for Postman testing.

---

## 1. High-Level System Dependency Flow

This flowchart illustrates the primary operational sequence required by the FinPilot AI backend:

```mermaid
flowchart TD
    %% Base Infrastructure
    A["1. GET /auth/csrf/<br/><b>Generates: {{csrf_token}}</b>"] --> B["2. POST /auth/register/ or 3. Login<br/><b>Establishes Session Cookie</b>"]
    B --> C["4. GET /auth/me/<br/><b>Captures: {{organization_id}}</b>"]

    %% Catalogs & Entities
    C --> D1["5. Module 05: GST Rates<br/><b>Captures: {{test_gst_rate_id}}</b>"]
    C --> D2["6. Module 04: Customers<br/><b>Captures: {{test_customer_id}}</b>"]
    D1 --> D3["7. Module 06: Products<br/><b>Captures: {{test_product_id}}</b>"]

    %% Core Transactional Engine
    D2 & D3 --> E1["8. Module 07: Invoices (Create)<br/><b>Captures: {{test_invoice_id}}</b>"]
    E1 --> E2["9. Module 08: Payments (Record & Allocate)<br/><b>Captures: {{test_payment_id}}, {{test_allocation_id}}</b>"]
    E2 --> E3["10. Module 08: Reverse Allocation<br/><b>Restores Invoice Balance</b>"]
    E3 --> E4["11. Module 07: Void Invoice<br/><b>Safely Cancels Invoice</b>"]

    %% Analytics & Downstream Intelligence
    E1 & E2 --> F1["12. Module 03: Dashboard & Aging Reports"]
    E1 & E2 --> F2["13. Module 11: Cash Flow Forecasts"]
    E1 & E2 --> F3["14. Module 09: AI Assistant Queries"]
    E1 & E2 --> F4["15. Module 15: CSV Exports"]

    %% Automation & Operations
    D2 & E1 --> G1["16. Module 12: Reminders<br/><b>Templates ➔ Policies ➔ Jobs</b>"]
    E1 & E2 --> G2["17. Module 13: Reconciliation<br/><b>Statement ➔ Mapping ➔ Matches</b>"]
    C --> G3["18. Module 14: Batch Invoice Imports<br/><b>Upload ➔ Preview ➔ Commit</b>"]

    %% Governance & Teardown
    C --> H1["19. Module 18: Platform Admin (Superuser)"]
    G1 & G2 & G3 --> Z["20. POST /auth/logout/<br/><b>Terminates Session (Final Step)</b>"]

    %% Styles
    classDef auth fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef catalog fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef tx fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef ops fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef danger fill:#ffebee,stroke:#c62828,stroke-width:2px;

    class A,B,C auth;
    class D1,D2,D3 catalog;
    class E1,E2,E3,E4 tx;
    class F1,F2,F3,F4,G1,G2,G3,H1 ops;
    class Z danger;
```

---

## 2. Dynamic Variable Handshake Map

This diagram details exactly which API populates which Postman environment variable, and which downstream APIs consume that variable:

```mermaid
graph LR
    subgraph Token_and_Org ["1. Security & Tenant Context"]
        CSRF_API["GET /auth/csrf/"] -->|Sets| CSRF["{{csrf_token}}"]
        ME_API["GET /auth/me/"] -->|Sets| ORG["{{organization_id}}"]
    end

    subgraph Master_Data ["2. Catalogs & Masters"]
        CSRF & ORG --> GST_CREATE["POST /gst-rates/"]
        GST_CREATE -->|Sets| GST_ID["{{test_gst_rate_id}}"]

        CSRF & ORG & GST_ID --> PROD_CREATE["POST /products/"]
        PROD_CREATE -->|Sets| PROD_ID["{{test_product_id}}"]

        CSRF & ORG --> CUST_CREATE["POST /customers/"]
        CUST_CREATE -->|Sets| CUST_ID["{{test_customer_id}}"]
    end

    subgraph Transaction_Core ["3. Financial Transactions"]
        CSRF & ORG & CUST_ID & PROD_ID --> INV_CREATE["POST /invoices/"]
        INV_CREATE -->|Sets| INV_ID["{{test_invoice_id}}"]

        CSRF & ORG & CUST_ID & INV_ID --> PAY_CREATE["POST /payments/"]
        PAY_CREATE -->|Sets| PAY_ID["{{test_payment_id}}"]
        PAY_CREATE -->|Sets| ALLOC_ID["{{test_allocation_id}}"]

        CSRF & ORG & PAY_ID & ALLOC_ID --> PAY_REV["POST /payments/.../reverse/"]
        CSRF & ORG & INV_ID --> INV_VOID["POST /invoices/.../void/"]
    end

    subgraph AR_Automation ["4. Automated Reminders"]
        CSRF & ORG --> TMPL_CREATE["POST /reminders/templates/"]
        TMPL_CREATE -->|Sets| TMPL_ID["{{test_reminder_template_id}}"]

        CSRF & ORG & TMPL_ID --> POL_CREATE["POST /reminders/policies/"]
        POL_CREATE -->|Sets| POL_ID["{{test_reminder_policy_id}}"]

        ORG --> JOBS_LIST["GET /reminders/jobs/"]
        JOBS_LIST -->|Sets| JOB_ID["{{test_reminder_job_id}}"]
    end

    subgraph Banking_and_Imports ["5. Reconciliation & Imports"]
        CSRF & ORG --> BANK_UP["POST /imports/bank-statements/"]
        BANK_UP -->|Sets| BANK_BATCH["{{test_bank_batch_id}}"]

        CSRF & ORG & BANK_BATCH --> BANK_CONF["POST /imports/.../confirm-mapping/"]
        ORG --> RECON_LIST["GET /reconciliation/"]
        RECON_LIST -->|Sets| RECON_ID["{{test_recon_match_id}}"]

        CSRF & ORG --> INV_UP["POST /imports/invoices/"]
        INV_UP -->|Sets| IMP_BATCH["{{test_import_batch_id}}"]
        CSRF & ORG & IMP_BATCH --> IMP_COMM["POST /imports/.../commit/"]
    end
```

---

## 3. The Two Fatal Execution Traps

### ⚠️ Trap 1: The Early Logout Trap
```
[Unsafe Flow]
  1. CSRF ──> 2. Login ──> 3. Get Me ──> 4. Logout ❌ ──> 5. List Customers 💥 (401 Unauthorized)

[Safe Flow]
  1. CSRF ──> 2. Login ──> 3. Get Me ──> [Run APIs 5 through 86] ──> 87. Logout ✅ (Session Safely Closed)
```
* **Why it fails**: Logging out immediately removes `sessionid` from the Postman cookie jar. Since Django does not use long-lived JWT headers, every subsequent request is rejected.

---

### ⚠️ Trap 2: The Invoice Void vs Payment Allocation Trap
```
[Unsafe Flow]
  Create Invoice ──> Void Invoice ❌ ──> Record Payment with Allocation 💥 (400 Bad Request)
  *Reason: Cannot allocate funds to an invoice marked as 'void'*

[Unsafe Flow 2]
  Create Invoice ──> Record Payment ──> Void Invoice ❌ 💥 (400 Bad Request)
  *Reason: Backend raises 'Reverse existing allocations before voiding this invoice'*

[Safe Flow]
  Create Invoice ──> Record Payment (with allocation) ──> Reverse Allocation ──> Void Invoice ✅
```
* **Code Constraint (`backend/core/views.py`)**:
  ```python
  active_allocs = invoice.allocations.filter(reversed_at__isnull=True)
  if active_allocs.exists():
      return Response({"detail": "Reverse existing allocations before voiding this invoice."}, status=400)
  ```

---

## 4. Module Dependency Matrix & Prerequisites

| Module Name | Folder # | Requires Session? | Requires CSRF? | Requires `X-Organization-ID`? | Internal Pre-Requisite Data |
|---|---|---|---|---|---|
| **01 - Authentication** | 01 | No (except Me/Logout) | Yes (for Register/Login/Logout) | Only for Logout | Backend reachable |
| **02 - Organizations** | 02 | Yes | Yes (for Create/Update) | Yes (except Create Org) | Active User Account |
| **03 - Dashboard & Reports** | 03 | Yes | No (`GET`) | Yes | Organization ID |
| **04 - Customers** | 04 | Yes | Yes (for Create/Update/Opt) | Yes | Organization ID |
| **05 - GST Rates** | 05 | Yes | Yes (for Create/Update/Act) | Yes | Organization ID |
| **06 - Products** | 06 | Yes | Yes (for Create/Update/Act) | Yes | Active GST Rate ID (`test_gst_rate_id`) |
| **07 - Invoices** | 07 | Yes | Yes (for Create/Update/Void) | Yes | Customer ID (`test_customer_id`), Product ID (`test_product_id`) |
| **08 - Payments** | 08 | Yes | Yes (for Record/Reverse) | Yes | Customer ID (`test_customer_id`), Invoice ID (`test_invoice_id`) |
| **09 - AI Assistant** | 09 | Yes | Yes (`POST`) | Yes | Organization ID, Active AI Provider Key (`OPENAI_API_KEY`) |
| **10 - Notifications** | 10 | Yes | Yes (for Mark Read) | Yes | Organization ID, Existing Notification ID |
| **11 - Forecast** | 11 | Yes | No (`GET`) | Yes | Organization ID, Invoices in Database |
| **12 - Reminders / Templates** | 12 | Yes | Yes (for Create/Update/Approve) | Yes | Organization ID |
| **12 - Reminders / Policies** | 12 | Yes | Yes (for Create/Update/Auto) | Yes | Reminder Template ID (`test_reminder_template_id`) |
| **12 - Reminders / Jobs** | 12 | Yes | Yes (for Approve/Reject) | Yes | Reminder Policy evaluated, Open Invoice |
| **13 - Reconciliation** | 13 | Yes | Yes (for Upload/Mapping/Match) | Yes | Bank Statement File (`.csv`/`.xlsx`), Invoice |
| **14 - Invoice Imports** | 14 | Yes | Yes (for Upload/Commit) | Yes | Invoice CSV/XLSX File, Organization ID |
| **15 - Exports** | 15 | Yes | No (`GET`) | Yes | Organization ID |
| **16 - Audit Log** | 16 | Yes | No (`GET`) | Yes | Organization ID |
| **17 - Subscriptions** | 17 | Yes | No (`GET`) | Yes | Organization ID |
| **18 - Platform Admin** | 18 | Yes (Superuser) | No (`GET`) | No | Django Staff/Superuser Account |
| **19 - OpenAPI Schema** | 19 | No | No (`GET`) | No | None |

---

## 5. How to Obtain and Reuse IDs Manually

If you need to manually inspect or override any variable in Postman:

1. **Accessing the Postman Environment**:
   * Click the eye icon (`Quick Look`) or click **Environments** in the left sidebar -> Select `FinPilot AI - Local Dev`.
2. **Finding IDs in Responses**:
   * **Organization ID**: Found in `GET /api/v1/auth/me/` under `organizations[0].id`.
   * **Customer ID**: Found in `POST /api/v1/customers/` response under `id`.
   * **Product ID**: Found in `POST /api/v1/products/` response under `id`.
   * **Invoice ID**: Found in `POST /api/v1/invoices/` response under `id`.
   * **Payment ID**: Found in `POST /api/v1/payments/` response under `id`.
   * **Allocation ID**: Found in `POST /api/v1/payments/` response under `allocations[0].id`.
   * **Template ID**: Found in `POST /api/v1/reminders/templates/` response under `id`.
   * **Policy ID**: Found in `POST /api/v1/reminders/policies/` response under `id`.
   * **Bank Statement Batch ID**: Found in `POST /api/v1/imports/bank-statements/` response under `batch_id`.
   * **Reconciliation Match ID**: Found in `GET /api/v1/reconciliation/` response as first item's `id`.
   * **Import Batch ID**: Found in `POST /api/v1/imports/invoices/` response under `batch_id`.


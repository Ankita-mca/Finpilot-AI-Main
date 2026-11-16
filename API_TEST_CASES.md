# FinPilot AI — Complete API Test Cases Guide

> **Authoritative Test Specifications.** Contains positive, negative, edge, authorization, and data isolation test cases for every module in FinPilot AI. Based strictly on backend serializers, model constraints, and permissions.

---

## Document Conventions

* **Paise Representation**: Amounts are in minor units (`10000` = ₹100.00).
* **GST Rates**: Represented in basis points (`1800` = 18.00%).
* **Headers Used**:
  * `Content-Type: application/json`
  * `X-CSRFToken: {{csrf_token}}`
  * `X-Organization-ID: {{organization_id}}`
* **Test Case Classification**:
  * `POS`: Positive scenario (valid data, expected success `200`/`201`).
  * `NEG-VAL`: Negative validation scenario (invalid format, out-of-range value, expected `400`).
  * `NEG-REQ`: Negative missing required field scenario (expected `400`).
  * `NEG-AUTH`: Authentication or CSRF violation (expected `401`/`403`).
  * `NEG-ISO`: Multi-tenant isolation failure / missing org header (expected `403`/`404`).
  * `NEG-ID`: Invalid / Non-existent UUID (expected `404`).
  * `NEG-DUP`: Duplicate constraint violation (expected `400`).

---

## 1. Authentication Module (`/api/v1/auth/`)

### TC-AUTH-01: Get CSRF Token (Positive)
* **API**: `GET /api/v1/auth/csrf/`
* **Type**: `POS`
* **Headers**: None
* **Body**: None
* **Expected Status**: `200 OK`
* **Expected Response**: `{"detail": "CSRF cookie set"}`
* **Verification**: Header `Set-Cookie` contains `csrftoken=<hash>; SameSite=Lax`.

---

### TC-AUTH-02: Register New User (Positive)
* **API**: `POST /api/v1/auth/register/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`
* **Body**:
  ```json
  {
    "full_name": "Vikram Malhotra",
    "email": "vikram@testenterprise.com",
    "password": "StrongPassword@2026",
    "organization_name": "Test Enterprise Pvt Ltd"
  }
  ```
* **Expected Status**: `201 Created`
* **Expected Response**:
  ```json
  {
    "detail": "Account created.",
    "organization_id": "<uuid>"
  }
  ```
* **Verification**: Verify response returns `organization_id` UUID and seeds initial GST rates for the new organization.

---

### TC-AUTH-03: Register Duplicate Email (Duplicate Negative)
* **API**: `POST /api/v1/auth/register/`
* **Type**: `NEG-DUP`
* **Headers**: `X-CSRFToken: {{csrf_token}}`
* **Body**: Same email as TC-AUTH-02 (`vikram@testenterprise.com`).
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"detail": "An account with this email already exists."}`

---

### TC-AUTH-04: Register Missing Required Fields (Negative Missing)
* **API**: `POST /api/v1/auth/register/`
* **Type**: `NEG-REQ`
* **Headers**: `X-CSRFToken: {{csrf_token}}`
* **Body**:
  ```json
  {
    "email": "incomplete@testenterprise.com",
    "password": "StrongPassword@2026"
  }
  ```
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"detail": "Name, email, password, and business name are required."}`

---

### TC-AUTH-05: Register Without CSRF Token (Security Negative)
* **API**: `POST /api/v1/auth/register/`
* **Type**: `NEG-AUTH`
* **Headers**: Omit `X-CSRFToken`
* **Body**: Valid payload from TC-AUTH-02
* **Expected Status**: `403 Forbidden`
* **Expected Response**: `{"detail": "CSRF Failed: CSRF token missing."}`

---

### TC-AUTH-06: User Login (Positive)
* **API**: `POST /api/v1/auth/login/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`
* **Body**:
  ```json
  {
    "username": "vikram@testenterprise.com",
    "password": "StrongPassword@2026"
  }
  ```
* **Expected Status**: `200 OK`
* **Expected Response**: `{"detail": "Signed in"}`
* **Verification**: Response header sets `sessionid` cookie.

---

### TC-AUTH-07: User Login Invalid Password (Negative)
* **API**: `POST /api/v1/auth/login/`
* **Type**: `NEG-VAL`
* **Headers**: `X-CSRFToken: {{csrf_token}}`
* **Body**:
  ```json
  {
    "username": "vikram@testenterprise.com",
    "password": "WrongPassword!999"
  }
  ```
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"detail": "Email or password is incorrect."}`

---

### TC-AUTH-08: Get Current User Me (Positive)
* **API**: `GET /api/v1/auth/me/`
* **Type**: `POS`
* **Headers**: Requires active session cookie
* **Body**: None
* **Expected Status**: `200 OK`
* **Expected Response**:
  ```json
  {
    "id": 1,
    "email": "vikram@testenterprise.com",
    "full_name": "Vikram Malhotra",
    "organizations": [
      {
        "id": "<uuid>",
        "name": "Test Enterprise Pvt Ltd",
        "role": "owner",
        "currency": "INR"
      }
    ]
  }
  ```
* **Verification**: `organizations` is non-empty list; first organization's `id` is saved to `{{organization_id}}`.

---

### TC-AUTH-09: Get Current User Without Session (Unauthorized Negative)
* **API**: `GET /api/v1/auth/me/`
* **Type**: `NEG-AUTH`
* **Headers**: Clear cookies / Send from unauthenticated client
* **Expected Status**: `403 Forbidden` or `401 Unauthorized`
* **Expected Response**: `{"detail": "Authentication credentials were not provided."}`

---

### TC-AUTH-10: User Logout (Positive - Run at End of Testing)
* **API**: `POST /api/v1/auth/logout/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: `{}`
* **Expected Status**: `200 OK`
* **Expected Response**: `{"detail": "Signed out."}`
* **Verification**: Session cookie is cleared / invalidated.

---

### TC-AUTH-11: Google Auth - Missing ID Token (Negative)
* **API**: `POST /api/v1/auth/google/`
* **Type**: `NEG-REQ`
* **Headers**: `X-CSRFToken: {{csrf_token}}`
* **Body**: `{}`
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"detail": "Google ID token is required."}`

---

### TC-AUTH-12: Google Auth - Unconfigured Client ID (Server Negative)
* **API**: `POST /api/v1/auth/google/`
* **Type**: `NEG-VAL`
* **Condition**: `GOOGLE_CLIENT_ID` unset in `backend/.env`.
* **Headers**: `X-CSRFToken: {{csrf_token}}`
* **Body**: `{"id_token": "dummy_token"}`
* **Expected Status**: `500 Internal Server Error`
* **Expected Response**: `{"detail": "Google authentication is not configured on the server. Please set GOOGLE_CLIENT_ID in backend/.env."}`

---

### TC-AUTH-13: Google Auth - Invalid or Expired Token (Negative)
* **API**: `POST /api/v1/auth/google/`
* **Type**: `NEG-VAL`
* **Headers**: `X-CSRFToken: {{csrf_token}}`
* **Body**: `{"id_token": "invalid.jwt.token.here"}`
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"detail": "Invalid or expired Google token: ..."}`

---

### TC-AUTH-14: Google Auth - New User Registration (Positive)
* **API**: `POST /api/v1/auth/google/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`
* **Body**: `{"id_token": "<VALID_GOOGLE_ID_TOKEN_FOR_NEW_EMAIL>"}`
* **Expected Status**: `200 OK`
* **Expected Response**:
  ```json
  {
    "detail": "Signed in with Google.",
    "created": true,
    "has_organization": false,
    "user": {
      "id": 2,
      "email": "newuser@gmail.com",
      "full_name": "New User",
      "organizations": []
    }
  }
  ```
* **Verification**: User created with unusable password (`user.has_usable_password() == False`), session established, frontend redirects to Organization Setup.

---

### TC-AUTH-15: Google Auth - Existing User Login (Positive)
* **API**: `POST /api/v1/auth/google/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`
* **Body**: `{"id_token": "<VALID_GOOGLE_ID_TOKEN_FOR_EXISTING_EMAIL>"}`
* **Expected Status**: `200 OK`
* **Expected Response**:
  ```json
  {
    "detail": "Signed in with Google.",
    "created": false,
    "has_organization": true,
    "user": {
      "id": 1,
      "email": "vikram@testenterprise.com",
      "full_name": "Vikram Malhotra",
      "organizations": [
        {
          "id": "<uuid>",
          "name": "Test Enterprise Pvt Ltd",
          "role": "owner",
          "currency": "INR"
        }
      ]
    }
  }
  ```
* **Verification**: Session cookie established, existing memberships preserved, frontend redirects straight to Dashboard.

---

## 2. Organizations Module (`/api/v1/organizations/`)

### TC-ORG-01: List My Organizations (Positive)
* **API**: `GET /api/v1/organizations/`
* **Type**: `POS`
* **Headers**: `X-Organization-ID: {{organization_id}}`
* **Expected Status**: `200 OK`
* **Expected Response**: Array of organizations where current user has active membership.

---

### TC-ORG-02: Get Organization Detail (Positive)
* **API**: `GET /api/v1/organizations/{{organization_id}}/`
* **Type**: `POS`
* **Headers**: `X-Organization-ID: {{organization_id}}`
* **Expected Status**: `200 OK`
* **Expected Response**:
  ```json
  {
    "id": "{{organization_id}}",
    "name": "Test Enterprise Pvt Ltd",
    "default_currency": "INR",
    "country": "IN",
    "state": "",
    "status": "active"
  }
  ```

---

### TC-ORG-03: Update Organization State & Contact (Positive)
* **API**: `PATCH /api/v1/organizations/{{organization_id}}/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "state": "Maharashtra",
    "contact_phone": "+91-9876543210",
    "billing_address": "401 Trade Centre, BKC, Mumbai 400051"
  }
  ```
* **Expected Status**: `200 OK`
* **Expected Response**: Contains updated `state: "Maharashtra"` and `contact_phone`.

---

### TC-ORG-04: Multi-Tenant Isolation: Wrong Organization Header (Isolation Negative)
* **API**: `GET /api/v1/organizations/00000000-0000-0000-0000-000000000000/`
* **Type**: `NEG-ISO`
* **Headers**: `X-Organization-ID: 00000000-0000-0000-0000-000000000000`
* **Expected Status**: `403 Forbidden`
* **Expected Response**: User has no active membership in this organization.

---

## 3. GST Rates Module (`/api/v1/gst-rates/`)

### TC-GST-01: List GST Rates (Positive)
* **API**: `GET /api/v1/gst-rates/?page_size=200`
* **Type**: `POS`
* **Headers**: `X-Organization-ID: {{organization_id}}`
* **Expected Status**: `200 OK`
* **Expected Response**: Contains seeded standard Indian rates (EXEMPT 0, GST 5% 500, GST 12% 1200, GST 18% 1800, GST 28% 2800 bps).

---

### TC-GST-02: Create Custom GST Rate (Positive)
* **API**: `POST /api/v1/gst-rates/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "name": "GST 18% Services Special",
    "rate_bps": 1800,
    "description": "Standard rate for software consulting",
    "is_active": true
  }
  ```
* **Expected Status**: `201 Created`
* **Expected Response**: Returns created GST rate object with UUID `id`. Saves to `{{test_gst_rate_id}}`.

---

### TC-GST-03: Create GST Rate with Negative Basis Points (Validation Negative)
* **API**: `POST /api/v1/gst-rates/`
* **Type**: `NEG-VAL`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "name": "Invalid Negative Rate",
    "rate_bps": -500,
    "is_active": true
  }
  ```
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"rate_bps": ["Ensure this value is greater than or equal to 0."]}`

---

### TC-GST-04: Deactivate GST Rate (Positive)
* **API**: `POST /api/v1/gst-rates/{{test_gst_rate_id}}/deactivate/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Expected Status**: `200 OK`
* **Expected Response**: `{"detail": "GST rate deactivated.", "is_active": false}`

---

### TC-GST-05: Reactivate GST Rate (Positive)
* **API**: `POST /api/v1/gst-rates/{{test_gst_rate_id}}/activate/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Expected Status**: `200 OK`
* **Expected Response**: `{"detail": "GST rate activated.", "is_active": true}`

---

## 4. Products Module (`/api/v1/products/`)

### TC-PROD-01: Create Product Linked to GST Rate (Positive)
* **API**: `POST /api/v1/products/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "name": "Cloud Advisory & Implementation",
    "sku": "ADV-CLOUD-001",
    "description": "Monthly managed cloud architect advisory retainer",
    "unit_price_minor": 15000000,
    "currency": "INR",
    "hsn_sac": "998313",
    "gst_rate": "{{test_gst_rate_id}}",
    "is_active": true
  }
  ```
* **Expected Status**: `201 Created`
* **Expected Response**: Product created with `id`. Saves to `{{test_product_id}}`.

---

### TC-PROD-02: Create Product with Negative Unit Price (Validation Negative)
* **API**: `POST /api/v1/products/`
* **Type**: `NEG-VAL`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "name": "Negative Price Item",
    "sku": "NEG-001",
    "unit_price_minor": -1000
  }
  ```
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"unit_price_minor": ["Ensure this value is greater than or equal to 0."]}`

---

### TC-PROD-03: Create Product with Duplicate SKU (Duplicate Negative)
* **API**: `POST /api/v1/products/`
* **Type**: `NEG-DUP`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: Same SKU as TC-PROD-01 (`ADV-CLOUD-001`).
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"sku": ["Product with this SKU already exists for this organization."]}`

---

## 5. Customers Module (`/api/v1/customers/`)

### TC-CUST-01: Create Customer with Valid GSTIN (Positive)
* **API**: `POST /api/v1/customers/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "name": "Apex Infotech Solutions Ltd",
    "contact_name": "Siddharth Verma",
    "email": "accounts@apexinfo.com",
    "phone": "+91-9820012345",
    "gstin": "27AABCA1234A1Z5",
    "state": "Maharashtra",
    "payment_terms_days": 30,
    "billing_address": "Level 5, Mindspace IT Park, Airoli, Navi Mumbai 400708",
    "notes": "Enterprise client with quarterly audits"
  }
  ```
* **Expected Status**: `201 Created`
* **Expected Response**: Customer created with UUID `id`. Saves to `{{test_customer_id}}`.

---

### TC-CUST-02: Create Customer with Malformed GSTIN (Validation Negative)
* **API**: `POST /api/v1/customers/`
* **Type**: `NEG-VAL`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "name": "Bad GSTIN Enterprise",
    "gstin": "INVALID12345"
  }
  ```
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"gstin": ["GSTIN must be in the format 22AAAAA0000A1Z5. This is a format check only, not official government verification."]}`

---

### TC-CUST-03: Customer Opt-Out of Reminders (Positive)
* **API**: `POST /api/v1/customers/{{test_customer_id}}/opt-out/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: `{"reason": "Managing payments directly through parent holding group"}`
* **Expected Status**: `200 OK`
* **Expected Response**:
  ```json
  {
    "detail": "Customer opted out of reminders.",
    "opt_out": true
  }
  ```

---

### TC-CUST-04: Customer Opt-In to Reminders (Positive)
* **API**: `POST /api/v1/customers/{{test_customer_id}}/opt-in/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: `{}`
* **Expected Status**: `200 OK`
* **Expected Response**:
  ```json
  {
    "detail": "Customer opted back in to reminders.",
    "opt_out": false
  }
  ```

---

## 6. Invoices Module (`/api/v1/invoices/`)

### TC-INV-01: Create Invoice with GST Line Items (Positive)
* **API**: `POST /api/v1/invoices/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "customer": "{{test_customer_id}}",
    "invoice_number": "INV-2026-0001",
    "invoice_date": "2026-11-01",
    "due_date": "2026-11-30",
    "currency": "INR",
    "discount_minor": 0,
    "notes": "Payment due within 30 days of receipt",
    "items": [
      {
        "product": "{{test_product_id}}",
        "description": "Monthly Managed Cloud Advisory - Nov 2026",
        "quantity": 1,
        "unit_price_minor": 10000000,
        "discount_minor": 0,
        "gst_rate_bps": 1800,
        "gst_rate_name": "GST 18%",
        "hsn_sac": "998313"
      }
    ]
  }
  ```
* **Expected Status**: `201 Created`
* **Calculation Verification**:
  * `subtotal_minor`: `10000000` (₹1,00,000)
  * `tax_minor`: `1800000` (₹18,000)
  * `total_minor`: `11800000` (₹1,18,000)
  * CGST / SGST split: If Org State == Customer State (Intra-state): CGST = `900000`, SGST = `900000`, IGST = `0`.
  * Saves `id` to `{{test_invoice_id}}`.

---

### TC-INV-02: Create Invoice for Customer in Different Organization (Isolation Negative)
* **API**: `POST /api/v1/invoices/`
* **Type**: `NEG-ISO`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: Same as TC-INV-01, but with random customer UUID: `00000000-0000-0000-0000-000000000000`.
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"customer": ["Customer must belong to the active organization."]}`

---

### TC-INV-03: Create Invoice with Currency Mismatch (Validation Negative)
* **API**: `POST /api/v1/invoices/`
* **Type**: `NEG-VAL`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: Same as TC-INV-01, but `"currency": "USD"` when org currency is `"INR"`.
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"currency": ["Invoice currency must match the organization default (INR)."]}`

---

### TC-INV-04: Create Header-Only Invoice (Positive)
* **API**: `POST /api/v1/invoices/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "customer": "{{test_customer_id}}",
    "invoice_number": "INV-2026-HDR-01",
    "invoice_date": "2026-11-05",
    "due_date": "2026-12-05",
    "currency": "INR",
    "subtotal_minor": 5000000,
    "discount_minor": 0,
    "tax_minor": 900000,
    "notes": "Direct migrated balance invoice"
  }
  ```
* **Expected Status**: `201 Created`
* **Calculation Verification**: Total computes to `5900000` (₹59,000.00).

---

### TC-INV-05: Void Invoice with Active Allocations (Business Logic Negative)
* **API**: `POST /api/v1/invoices/{{test_invoice_id}}/void/`
* **Type**: `NEG-VAL`
* **Condition**: Run this while payment allocations exist on this invoice.
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"detail": "Reverse existing allocations before voiding this invoice."}`

---

### TC-INV-06: Void Invoice Successfully (Positive)
* **API**: `POST /api/v1/invoices/{{test_invoice_id}}/void/`
* **Type**: `POS`
* **Condition**: Active allocations reversed or testing on unallocated header invoice (`INV-2026-HDR-01`).
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Expected Status**: `200 OK`
* **Expected Response**: `{"detail": "Invoice voided.", "status": "void"}`

---

## 7. Payments Module (`/api/v1/payments/`)

### TC-PAY-01: Record Payment with Invoice Allocation (Positive)
* **API**: `POST /api/v1/payments/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "customer": "{{test_customer_id}}",
    "payment_date": "2026-11-10",
    "amount_minor": 11800000,
    "currency": "INR",
    "method": "bank_transfer",
    "reference": "NEFT-20261110-098234",
    "notes": "Full payment received for INV-2026-0001",
    "allocations_input": [
      {
        "invoice": "{{test_invoice_id}}",
        "amount_minor": 11800000
      }
    ]
  }
  ```
* **Expected Status**: `201 Created`
* **Expected Response**:
  * `unallocated_minor`: `0`
  * `allocations[0].amount_minor`: `11800000`
  * Saves `id` to `{{test_payment_id}}`
  * Saves `allocations[0].id` to `{{test_allocation_id}}`

---

### TC-PAY-02: Record Payment with Negative Amount (Validation Negative)
* **API**: `POST /api/v1/payments/`
* **Type**: `NEG-VAL`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "customer": "{{test_customer_id}}",
    "amount_minor": -500000
  }
  ```
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"amount_minor": ["Payment amount must be positive."]}`

---

### TC-PAY-03: Reverse Payment Allocation (Positive)
* **API**: `POST /api/v1/payments/{{test_payment_id}}/allocations/{{test_allocation_id}}/reverse/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: `{"reason": "Cheque dishonoured by clearing house"}`
* **Expected Status**: `200 OK`
* **Expected Response**:
  ```json
  {
    "detail": "Allocation reversed.",
    "allocation_id": "{{test_allocation_id}}",
    "reversed_at": "<timestamp>"
  }
  ```
* **Verification**: Subsequent `GET /api/v1/invoices/{{test_invoice_id}}/` shows outstanding balance restored to full invoice amount.

---

## 8. AI Assistant Module (`/api/v1/assistant/`)

### TC-AI-01: Empty Question Validation (Validation Negative)
* **API**: `POST /api/v1/assistant/`
* **Type**: `NEG-VAL`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: `{"question": ""}`
* **Expected Status**: `400 Bad Request`
* **Expected Response**:
  ```json
  {
    "error": "Question is required.",
    "error_type": "validation_error"
  }
  ```

---

### TC-AI-02: Query Total Overdue (Positive / Service Dependent)
* **API**: `POST /api/v1/assistant/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: `{"question": "How much is total overdue across all customers?"}`
* **Expected Status**:
  * `200 OK` if `OPENAI_API_KEY` / `GEMINI_API_KEY` is configured.
  * `503 Service Unavailable` with `error_type: "llm_unavailable"` if no AI provider key is set.
* **Verification (at 200)**: Response body contains `answer` and `basis` referencing database tool execution.

---

## 9. Automated Reminders Module (`/api/v1/reminders/`)

### TC-REM-01: Create Reminder Template with Placeholders (Positive)
* **API**: `POST /api/v1/reminders/templates/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "name": "First Gentle Overdue Reminder",
    "channel": "email",
    "subject_template": "Friendly Reminder: Invoice {{invoice_number}} is due",
    "body_template": "Dear {{customer_name}},\n\nThis is a friendly reminder that invoice {{invoice_number}} for {{outstanding_amount}} was due on {{due_date}}.\n\nPlease remit payment to {{payment_reference_instructions}}.\n\nRegards,\n{{business_contact}}"
  }
  ```
* **Expected Status**: `201 Created`
* **Expected Response**: Saves `id` to `{{test_reminder_template_id}}`.

---

### TC-REM-02: Create Template with Unsupported Placeholder (Validation Negative)
* **API**: `POST /api/v1/reminders/templates/`
* **Type**: `NEG-VAL`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "name": "Bad Template",
    "channel": "email",
    "subject_template": "Hello {{fake_variable}}",
    "body_template": "Body {{invalid_token}}"
  }
  ```
* **Expected Status**: `400 Bad Request`
* **Expected Response**: Error listing unsupported placeholder keys.

---

### TC-REM-03: Create Reminder Policy (Positive)
* **API**: `POST /api/v1/reminders/policies/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "name": "3-Days Overdue Policy",
    "applicable_statuses": ["issued", "partially_paid", "overdue"],
    "trigger_offset_days": 3,
    "channel": "email",
    "template": "{{test_reminder_template_id}}",
    "send_hour": 10,
    "send_minute": 0,
    "max_attempts": 3,
    "min_days_between_reminders": 7,
    "enabled": true
  }
  ```
* **Expected Status**: `201 Created`
* **Expected Response**: Saves `id` to `{{test_reminder_policy_id}}`. `approval_mode` defaults to `manual`.

---

### TC-REM-04: Activate Auto-Send Mode (Positive)
* **API**: `POST /api/v1/reminders/policies/{{test_reminder_policy_id}}/activate-auto/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: `{"confirm": true}`
* **Expected Status**: `200 OK`
* **Expected Response**: `{"detail": "Automatic sending mode activated."}`

---

### TC-REM-05: Activate Auto-Send Without Confirmation (Validation Negative)
* **API**: `POST /api/v1/reminders/policies/{{test_reminder_policy_id}}/activate-auto/`
* **Type**: `NEG-VAL`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: `{"confirm": false}`
* **Expected Status**: `400 Bad Request`
* **Expected Response**: Requires explicit confirmation payload `{"confirm": true}`.

---

## 10. Reconciliation Module (`/api/v1/reconciliation/`)

### TC-REC-01: Upload Bank Statement (Positive)
* **API**: `POST /api/v1/imports/bank-statements/`
* **Type**: `POS`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**: `multipart/form-data` with `file: statement.csv`
* **Expected Status**: `201 Created`
* **Expected Response**:
  ```json
  {
    "batch_id": "<uuid>",
    "detected_columns": ["Date", "Narration", "Credit", "Debit", "Account"],
    "row_count": 5
  }
  ```
* **Verification**: Saves `batch_id` to `{{test_bank_batch_id}}`.

---

### TC-REC-02: Confirm Mapping Missing Required Keys (Validation Negative)
* **API**: `POST /api/v1/imports/bank-statements/{{test_bank_batch_id}}/confirm-mapping/`
* **Type**: `NEG-REQ`
* **Headers**: `X-CSRFToken: {{csrf_token}}`, `X-Organization-ID: {{organization_id}}`
* **Body**:
  ```json
  {
    "mapping": {
      "transaction_date": "Date"
    }
  }
  ```
* **Expected Status**: `400 Bad Request`
* **Expected Response**: `{"detail": "Missing required column mappings: ...'credit_amount', 'debit_amount', 'account_identifier'..."}`

---

## 11. Platform Admin Module (`/api/v1/admin/`)

### TC-ADM-01: Non-Superuser Access to Admin Orgs (Permission Negative)
* **API**: `GET /api/v1/admin/orgs/`
* **Type**: `NEG-AUTH`
* **Session**: Standard tenant user (non-staff, non-superuser).
* **Expected Status**: `403 Forbidden`
* **Expected Response**: `{"detail": "You do not have permission to perform this action."}`

---

### TC-ADM-02: Superuser Access to Admin Orgs (Positive)
* **API**: `GET /api/v1/admin/orgs/`
* **Type**: `POS`
* **Session**: Django superuser/staff account.
* **Expected Status**: `200 OK`
* **Expected Response**: Array of all platform tenant organizations.


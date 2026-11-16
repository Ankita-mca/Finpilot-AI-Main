# FinPilot AI — Complete API Testing Tracker & Checklist

> **Interactive API Quality Assurance Checklist.** Use this document to record the progress and results of executing all 87 Postman requests in the recommended sequential flow.

---

## 1. Testing Progress Dashboard

| Metric | Target | Current Status |
|---|---|---|
| **Total Test Steps** | 87 | 87 |
| **Passed (`PASSED`)** | 87 | `0` |
| **Failed (`FAILED`)** | 0 | `0` |
| **Blocked (`BLOCKED`)** | 0 | `0` |
| **Not Tested (`NOT TESTED`)** | 0 | `87` |
| **Overall Completion** | 100% | **0%** |

*Legend*:
* `PASSED`: Status code and assertions matched expected output.
* `FAILED`: Returned unexpected error status or incorrect data structure.
* `BLOCKED`: Prerequisite data (e.g. no notification or no job exists) prevented execution.
* `NOT TESTED`: Awaiting execution.

---

## 2. Master Sequential Execution Checklist (87 Steps)

| Check | Step | Phase | Module | Postman API Name | Method | Endpoint | Status | Observed Status & Notes |
|:---:|:---:|---|---|---|:---:|---|:---:|---|
| [ ] | **01** | Phase 1: Bootstrapping | 01 - Authentication | `01 - Get CSRF Token` | `GET` | `/api/v1/auth/csrf/` | `NOT TESTED` | |
| [ ] | **02** | Phase 1: Bootstrapping | 01 - Authentication | `02 - Register New User` | `POST` | `/api/v1/auth/register/` | `NOT TESTED` | |
| [ ] | **03** | Phase 1: Bootstrapping | 01 - Authentication | `03 - Login` | `POST` | `/api/v1/auth/login/` | `NOT TESTED` | |
| [ ] | **04** | Phase 1: Bootstrapping | 01 - Authentication | `04 - Get Current User (me)` | `GET` | `/api/v1/auth/me/` | `NOT TESTED` | |
| [ ] | **05** | Phase 2: Organization | 02 - Organizations | `01 - List My Organizations` | `GET` | `/api/v1/organizations/` | `NOT TESTED` | |
| [ ] | **06** | Phase 2: Organization | 02 - Organizations | `03 - Get Organization Detail` | `GET` | `/api/v1/organizations/{{organization_id}}/` | `NOT TESTED` | |
| [ ] | **07** | Phase 2: Organization | 02 - Organizations | `04 - Update Organization (PATCH)` | `PATCH` | `/api/v1/organizations/{{organization_id}}/` | `NOT TESTED` | |
| [ ] | **08** | Phase 2: Organization | 02 - Organizations | `02 - Create Organization` | `POST` | `/api/v1/organizations/` | `NOT TESTED` | |
| [ ] | **09** | Phase 2: Organization | 02 - Organizations | `05 - List Team Members` | `GET` | `/api/v1/members/` | `NOT TESTED` | |
| [ ] | **10** | Phase 3: Financial Catalogs | 05 - GST Rates | `01 - List GST Rates` | `GET` | `/api/v1/gst-rates/?page_size=200` | `NOT TESTED` | |
| [ ] | **11** | Phase 3: Financial Catalogs | 05 - GST Rates | `02 - Create GST Rate` | `POST` | `/api/v1/gst-rates/` | `NOT TESTED` | |
| [ ] | **12** | Phase 3: Financial Catalogs | 05 - GST Rates | `03 - Get GST Rate Detail` | `GET` | `/api/v1/gst-rates/{{test_gst_rate_id}}/` | `NOT TESTED` | |
| [ ] | **13** | Phase 3: Financial Catalogs | 05 - GST Rates | `04 - Update GST Rate (PATCH)` | `PATCH` | `/api/v1/gst-rates/{{test_gst_rate_id}}/` | `NOT TESTED` | |
| [ ] | **14** | Phase 3: Financial Catalogs | 05 - GST Rates | `05 - Deactivate GST Rate` | `POST` | `/api/v1/gst-rates/{{test_gst_rate_id}}/deactivate/` | `NOT TESTED` | |
| [ ] | **15** | Phase 3: Financial Catalogs | 05 - GST Rates | `06 - Activate GST Rate` | `POST` | `/api/v1/gst-rates/{{test_gst_rate_id}}/activate/` | `NOT TESTED` | |
| [ ] | **16** | Phase 3: Financial Catalogs | 06 - Products | `01 - List Products` | `GET` | `/api/v1/products/?page_size=200` | `NOT TESTED` | |
| [ ] | **17** | Phase 3: Financial Catalogs | 06 - Products | `02 - Create Product` | `POST` | `/api/v1/products/` | `NOT TESTED` | |
| [ ] | **18** | Phase 3: Financial Catalogs | 06 - Products | `03 - Get Product Detail` | `GET` | `/api/v1/products/{{test_product_id}}/` | `NOT TESTED` | |
| [ ] | **19** | Phase 3: Financial Catalogs | 06 - Products | `04 - Update Product (PATCH)` | `PATCH` | `/api/v1/products/{{test_product_id}}/` | `NOT TESTED` | |
| [ ] | **20** | Phase 3: Financial Catalogs | 06 - Products | `05 - Deactivate Product` | `POST` | `/api/v1/products/{{test_product_id}}/deactivate/` | `NOT TESTED` | |
| [ ] | **21** | Phase 3: Financial Catalogs | 06 - Products | `06 - Activate Product` | `POST` | `/api/v1/products/{{test_product_id}}/activate/` | `NOT TESTED` | |
| [ ] | **22** | Phase 4: Customers | 04 - Customers | `01 - List Customers` | `GET` | `/api/v1/customers/?page_size=25` | `NOT TESTED` | |
| [ ] | **23** | Phase 4: Customers | 04 - Customers | `02 - Create Customer` | `POST` | `/api/v1/customers/` | `NOT TESTED` | |
| [ ] | **24** | Phase 4: Customers | 04 - Customers | `03 - Get Customer Detail` | `GET` | `/api/v1/customers/{{test_customer_id}}/` | `NOT TESTED` | |
| [ ] | **25** | Phase 4: Customers | 04 - Customers | `04 - Update Customer (PATCH)` | `PATCH` | `/api/v1/customers/{{test_customer_id}}/` | `NOT TESTED` | |
| [ ] | **26** | Phase 4: Customers | 04 - Customers | `05 - Full Update Customer (PUT)` | `PUT` | `/api/v1/customers/{{test_customer_id}}/` | `NOT TESTED` | |
| [ ] | **27** | Phase 4: Customers | 04 - Customers | `06 - Customer Opt-Out of Reminders` | `POST` | `/api/v1/customers/{{test_customer_id}}/opt-out/` | `NOT TESTED` | |
| [ ] | **28** | Phase 4: Customers | 04 - Customers | `07 - Customer Opt-In to Reminders` | `POST` | `/api/v1/customers/{{test_customer_id}}/opt-in/` | `NOT TESTED` | |
| [ ] | **29** | Phase 5: Invoicing Engine | 07 - Invoices | `01 - List Invoices` | `GET` | `/api/v1/invoices/?page_size=25` | `NOT TESTED` | |
| [ ] | **30** | Phase 5: Invoicing Engine | 07 - Invoices | `02 - Create Invoice (with GST line items)` | `POST` | `/api/v1/invoices/` | `NOT TESTED` | |
| [ ] | **31** | Phase 5: Invoicing Engine | 07 - Invoices | `03 - Create Invoice (header-only, no line items)` | `POST` | `/api/v1/invoices/` | `NOT TESTED` | |
| [ ] | **32** | Phase 5: Invoicing Engine | 07 - Invoices | `04 - Get Invoice Detail` | `GET` | `/api/v1/invoices/{{test_invoice_id}}/` | `NOT TESTED` | |
| [ ] | **33** | Phase 5: Invoicing Engine | 07 - Invoices | `05 - Update Invoice (PUT - Full)` | `PUT` | `/api/v1/invoices/{{test_invoice_id}}/` | `NOT TESTED` | |
| [ ] | **34** | Phase 6: Payment Processing | 08 - Payments | `01 - List Payments` | `GET` | `/api/v1/payments/?page_size=25` | `NOT TESTED` | |
| [ ] | **35** | Phase 6: Payment Processing | 08 - Payments | `02 - Record Payment (with allocation)` | `POST` | `/api/v1/payments/` | `NOT TESTED` | |
| [ ] | **36** | Phase 6: Payment Processing | 08 - Payments | `03 - Record Payment (no allocation)` | `POST` | `/api/v1/payments/` | `NOT TESTED` | |
| [ ] | **37** | Phase 6: Payment Processing | 08 - Payments | `04 - Get Payment Detail` | `GET` | `/api/v1/payments/{{test_payment_id}}/` | `NOT TESTED` | |
| [ ] | **38** | Phase 6: Payment Processing | 08 - Payments | `05 - Reverse Payment Allocation` | `POST` | `/api/v1/payments/{{test_payment_id}}/allocations/{{test_allocation_id}}/reverse/` | `NOT TESTED` | |
| [ ] | **39** | Phase 7: Invoice Cancellation | 07 - Invoices | `06 - Void Invoice` | `POST` | `/api/v1/invoices/{{test_invoice_id}}/void/` | `NOT TESTED` | |
| [ ] | **40** | Phase 8: Financial Intelligence | 03 - Dashboard & Reports | `01 - Get Dashboard` | `GET` | `/api/v1/dashboard/` | `NOT TESTED` | |
| [ ] | **41** | Phase 8: Financial Intelligence | 03 - Dashboard & Reports | `02 - Aging Report (Today)` | `GET` | `/api/v1/reports/aging/` | `NOT TESTED` | |
| [ ] | **42** | Phase 8: Financial Intelligence | 03 - Dashboard & Reports | `03 - Aging Report (Custom Date)` | `GET` | `/api/v1/reports/aging/?as_of=2026-10-31` | `NOT TESTED` | |
| [ ] | **43** | Phase 9: Cash Flow Forecasting | 11 - Forecast | `01 - Forecast (30 days, due date)` | `GET` | `/api/v1/forecasts/?period=30&timing=due_date` | `NOT TESTED` | |
| [ ] | **44** | Phase 9: Cash Flow Forecasting | 11 - Forecast | `02 - Forecast (7 days, historical delay)` | `GET` | `/api/v1/forecasts/?period=7&timing=historical_delay` | `NOT TESTED` | |
| [ ] | **45** | Phase 9: Cash Flow Forecasting | 11 - Forecast | `03 - Forecast (60 days, custom offset)` | `GET` | `/api/v1/forecasts/?period=60&timing=custom_offset&offset=7` | `NOT TESTED` | |
| [ ] | **46** | Phase 10: AI Assistant | 09 - AI Assistant | `04 - Validation Error Test (empty question)` | `POST` | `/api/v1/assistant/` | `NOT TESTED` | |
| [ ] | **47** | Phase 10: AI Assistant | 09 - AI Assistant | `01 - Ask a Question` | `POST` | `/api/v1/assistant/` | `NOT TESTED` | |
| [ ] | **48** | Phase 10: AI Assistant | 09 - AI Assistant | `02 - Ask About Top Overdue Customers` | `POST` | `/api/v1/assistant/` | `NOT TESTED` | |
| [ ] | **49** | Phase 10: AI Assistant | 09 - AI Assistant | `03 - Ask About Cash Flow Forecast` | `POST` | `/api/v1/assistant/` | `NOT TESTED` | |
| [ ] | **50** | Phase 11: Notification Center | 10 - Notifications | `01 - List Notifications` | `GET` | `/api/v1/notifications/` | `NOT TESTED` | |
| [ ] | **51** | Phase 11: Notification Center | 10 - Notifications | `02 - Mark Single Notification Read` | `POST` | `/api/v1/notifications/{{test_notification_id}}/read/` | `NOT TESTED` | |
| [ ] | **52** | Phase 11: Notification Center | 10 - Notifications | `03 - Mark All Notifications Read` | `POST` | `/api/v1/notifications/mark-all-read/` | `NOT TESTED` | |
| [ ] | **53** | Phase 12: Reminders Engine | 12 - Reminders / Templates | `01 - List Templates` | `GET` | `/api/v1/reminders/templates/` | `NOT TESTED` | |
| [ ] | **54** | Phase 12: Reminders Engine | 12 - Reminders / Templates | `02 - Create Template` | `POST` | `/api/v1/reminders/templates/` | `NOT TESTED` | |
| [ ] | **55** | Phase 12: Reminders Engine | 12 - Reminders / Templates | `03 - Get Template Detail` | `GET` | `/api/v1/reminders/templates/{{test_reminder_template_id}}/` | `NOT TESTED` | |
| [ ] | **56** | Phase 12: Reminders Engine | 12 - Reminders / Templates | `04 - Update Template (PATCH)` | `PATCH` | `/api/v1/reminders/templates/{{test_reminder_template_id}}/` | `NOT TESTED` | |
| [ ] | **57** | Phase 12: Reminders Engine | 12 - Reminders / Templates | `05 - Approve Template Revision` | `POST` | `/api/v1/reminders/templates/{{test_reminder_template_id}}/approve-revision/` | `NOT TESTED` | |
| [ ] | **58** | Phase 12: Reminders Engine | 12 - Reminders / Policies | `01 - List Policies` | `GET` | `/api/v1/reminders/policies/` | `NOT TESTED` | |
| [ ] | **59** | Phase 12: Reminders Engine | 12 - Reminders / Policies | `02 - Create Policy` | `POST` | `/api/v1/reminders/policies/` | `NOT TESTED` | |
| [ ] | **60** | Phase 12: Reminders Engine | 12 - Reminders / Policies | `03 - Get Policy Detail` | `GET` | `/api/v1/reminders/policies/{{test_reminder_policy_id}}/` | `NOT TESTED` | |
| [ ] | **61** | Phase 12: Reminders Engine | 12 - Reminders / Policies | `04 - Activate Auto-Send Mode` | `POST` | `/api/v1/reminders/policies/{{test_reminder_policy_id}}/activate-auto/` | `NOT TESTED` | |
| [ ] | **62** | Phase 12: Reminders Engine | 12 - Reminders / Policies | `05 - Deactivate Auto-Send Mode` | `POST` | `/api/v1/reminders/policies/{{test_reminder_policy_id}}/deactivate-auto/` | `NOT TESTED` | |
| [ ] | **63** | Phase 12: Reminders Engine | 12 - Reminders / Jobs | `01 - List Reminder Jobs` | `GET` | `/api/v1/reminders/jobs/` | `NOT TESTED` | |
| [ ] | **64** | Phase 12: Reminders Engine | 12 - Reminders / Jobs | `02 - Get Reminder Job Detail` | `GET` | `/api/v1/reminders/jobs/{{test_reminder_job_id}}/` | `NOT TESTED` | |
| [ ] | **65** | Phase 12: Reminders Engine | 12 - Reminders / Jobs | `03 - Approve Reminder Job` | `POST` | `/api/v1/reminders/jobs/{{test_reminder_job_id}}/approve/` | `NOT TESTED` | |
| [ ] | **66** | Phase 12: Reminders Engine | 12 - Reminders / Jobs | `04 - Reject Reminder Job` | `POST` | `/api/v1/reminders/jobs/{{test_reminder_job_id}}/reject/` | `NOT TESTED` | |
| [ ] | **67** | Phase 13: Reconciliation | 13 - Reconciliation | `01 - Upload Bank Statement` | `POST` | `/api/v1/imports/bank-statements/` | `NOT TESTED` | |
| [ ] | **68** | Phase 13: Reconciliation | 13 - Reconciliation | `02 - Confirm Column Mapping` | `POST` | `/api/v1/imports/bank-statements/{{test_bank_batch_id}}/confirm-mapping/` | `NOT TESTED` | |
| [ ] | **69** | Phase 13: Reconciliation | 13 - Reconciliation | `03 - List Reconciliation Matches` | `GET` | `/api/v1/reconciliation/` | `NOT TESTED` | |
| [ ] | **70** | Phase 13: Reconciliation | 13 - Reconciliation | `04 - Confirm Reconciliation Match` | `POST` | `/api/v1/reconciliation/{{test_recon_match_id}}/confirm/` | `NOT TESTED` | |
| [ ] | **71** | Phase 13: Reconciliation | 13 - Reconciliation | `05 - Reject Reconciliation Match` | `POST` | `/api/v1/reconciliation/{{test_recon_match_id}}/reject/` | `NOT TESTED` | |
| [ ] | **72** | Phase 14: Batch Imports | 14 - Invoice Imports | `01 - Download CSV Template` | `GET` | `/api/v1/imports/invoice-template/csv/` | `NOT TESTED` | |
| [ ] | **73** | Phase 14: Batch Imports | 14 - Invoice Imports | `02 - Download XLSX Template` | `GET` | `/api/v1/imports/invoice-template/xlsx/` | `NOT TESTED` | |
| [ ] | **74** | Phase 14: Batch Imports | 14 - Invoice Imports | `03 - Upload Invoice File` | `POST` | `/api/v1/imports/invoices/` | `NOT TESTED` | |
| [ ] | **75** | Phase 14: Batch Imports | 14 - Invoice Imports | `04 - Get Batch Status & Preview` | `GET` | `/api/v1/imports/invoices/{{test_import_batch_id}}/` | `NOT TESTED` | |
| [ ] | **76** | Phase 14: Batch Imports | 14 - Invoice Imports | `05 - Commit Import Batch` | `POST` | `/api/v1/imports/invoices/{{test_import_batch_id}}/commit/` | `NOT TESTED` | |
| [ ] | **77** | Phase 15: Exports | 15 - Exports | `01 - Export Invoices (CSV)` | `GET` | `/api/v1/exports/invoices/?org={{organization_id}}` | `NOT TESTED` | |
| [ ] | **78** | Phase 15: Exports | 15 - Exports | `02 - Export Customers (CSV)` | `GET` | `/api/v1/exports/customers/?org={{organization_id}}` | `NOT TESTED` | |
| [ ] | **79** | Phase 15: Exports | 15 - Exports | `03 - Export Payments (CSV)` | `GET` | `/api/v1/exports/payments/?org={{organization_id}}` | `NOT TESTED` | |
| [ ] | **80** | Phase 16: Audit Trail | 16 - Audit Log | `01 - List Audit Logs` | `GET` | `/api/v1/audit-logs/` | `NOT TESTED` | |
| [ ] | **81** | Phase 16: Audit Trail | 17 - Subscriptions | `01 - Get Subscription Status` | `GET` | `/api/v1/subscriptions/` | `NOT TESTED` | |
| [ ] | **82** | Phase 17: Platform Admin | 18 - Platform Admin | `01 - List All Organizations` | `GET` | `/api/v1/admin/orgs/` | `NOT TESTED` | Requires superuser |
| [ ] | **83** | Phase 17: Platform Admin | 18 - Platform Admin | `02 - List All Users` | `GET` | `/api/v1/admin/users/` | `NOT TESTED` | Requires superuser |
| [ ] | **84** | Phase 17: Platform Admin | 18 - Platform Admin | `03 - Platform-Wide Audit Log` | `GET` | `/api/v1/admin/audit-logs/` | `NOT TESTED` | Requires superuser |
| [ ] | **85** | Phase 18: Documentation | 19 - OpenAPI Schema | `01 - OpenAPI Schema (JSON)` | `GET` | `/api/schema/` | `NOT TESTED` | |
| [ ] | **86** | Phase 18: Documentation | 19 - OpenAPI Schema | `02 - Swagger UI` | `GET` | `/api/schema/swagger-ui/` | `NOT TESTED` | |
| [ ] | **87** | Phase 19: Teardown | 01 - Authentication | `05 - Logout` | `POST` | `/api/v1/auth/logout/` | `NOT TESTED` | Terminates active session |


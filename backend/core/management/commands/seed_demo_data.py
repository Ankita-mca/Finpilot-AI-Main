import uuid
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Organization, Customer, Invoice, InvoiceItem, Payment, PaymentAllocation
from products.models import Product, GSTRate

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds sample customers, products, and invoices (including overdue invoices) for testing."

    def handle(self, *args, **options):
        org = Organization.objects.order_by("-created_at").first()
        if not org:
            self.stderr.write(self.style.ERROR("No organization found. Please sign up or create an organization first."))
            return

        user = User.objects.filter(memberships__organization=org).first() or User.objects.first()
        if not user:
            self.stderr.write(self.style.ERROR("No user found."))
            return

        self.stdout.write(f"Seeding demo financial data for organization: '{org.name}' ({org.id})")

        # 1. GST Rate
        gst_18, _ = GSTRate.objects.get_or_create(
            organization=org,
            rate_bps=1800,
            defaults={"name": "GST 18%", "active": True}
        )

        # 2. Customers
        c1, _ = Customer.objects.get_or_create(
            organization=org,
            name="Acme Tech Solutions",
            defaults={
                "email": "accounts@acmetech.example.com",
                "phone": "+91 9876543210",
                "billing_address": "Cyber City, Gurugram, HR",
                "gstin": "06AAAAA0000A1Z5"
            }
        )
        c2, _ = Customer.objects.get_or_create(
            organization=org,
            name="Bharat Enterprises",
            defaults={
                "email": "finance@bharatent.example.com",
                "phone": "+91 9811223344",
                "billing_address": "Andheri East, Mumbai, MH",
                "gstin": "27AAAAA0000A1Z5"
            }
        )
        c3, _ = Customer.objects.get_or_create(
            organization=org,
            name="Zenith Media Works",
            defaults={
                "email": "invoicing@zenithmedia.example.com",
                "phone": "+91 9822334455",
                "billing_address": "Indiranagar, Bengaluru, KA",
                "gstin": "29AAAAA0000A1Z5"
            }
        )

        # 3. Products
        p1, _ = Product.objects.get_or_create(
            organization=org,
            name="Cloud Consulting Services",
            defaults={
                "unit_price_minor": 5000000, # Rs. 50,000
                "gst_rate": gst_18,
                "hsn_sac": "998313"
            }
        )
        p2, _ = Product.objects.get_or_create(
            organization=org,
            name="Annual Software License",
            defaults={
                "unit_price_minor": 2500000, # Rs. 25,000
                "gst_rate": gst_18,
                "hsn_sac": "997331"
            }
        )

        today = date.today()

        # 4. Invoices
        demo_invoices = [
            {
                "num": "INV-2026-001",
                "cust": c1,
                "inv_date": today - timedelta(days=45),
                "due_date": today - timedelta(days=15), # OVERDUE by 15 days
                "desc": "Cloud Architecture & Migration - Month 1",
                "qty": 1,
                "price": 5000000,
                "status": Invoice.Status.ISSUED,
            },
            {
                "num": "INV-2026-002",
                "cust": c2,
                "inv_date": today - timedelta(days=35),
                "due_date": today - timedelta(days=5), # OVERDUE by 5 days
                "desc": "Annual Software License Subscription",
                "qty": 1,
                "price": 2500000,
                "status": Invoice.Status.ISSUED,
            },
            {
                "num": "INV-2026-003",
                "cust": c3,
                "inv_date": today - timedelta(days=10),
                "due_date": today + timedelta(days=20), # DUE in 20 days
                "desc": "Digital Marketing & Analytics Audit",
                "qty": 1,
                "price": 3000000,
                "status": Invoice.Status.ISSUED,
            },
            {
                "num": "INV-2026-004",
                "cust": c1,
                "inv_date": today - timedelta(days=60),
                "due_date": today - timedelta(days=30),
                "desc": "Discovery Workshop & Roadmap",
                "qty": 1,
                "price": 2000000,
                "status": Invoice.Status.ISSUED,
                "is_paid": True,
            },
        ]

        created_count = 0
        for data in demo_invoices:
            inv, created = Invoice.objects.get_or_create(
                organization=org,
                invoice_number=data["num"],
                defaults={
                    "customer": data["cust"],
                    "invoice_date": data["inv_date"],
                    "due_date": data["due_date"],
                    "currency": "INR",
                    "subtotal_minor": data["price"] * data["qty"],
                    "discount_minor": 0,
                    "tax_minor": int((data["price"] * data["qty"]) * 0.18),
                    "total_minor": int((data["price"] * data["qty"]) * 1.18),
                    "status": data["status"],
                    "source": Invoice.Source.MANUAL,
                    "created_by": user,
                    "notes": "Generated sample invoice for testing."
                }
            )
            if created:
                created_count += 1
                tax_amt = int((data["price"] * data["qty"]) * 0.18)
                cgst = tax_amt // 2
                sgst = tax_amt - cgst
                InvoiceItem.objects.create(
                    organization=org,
                    invoice=inv,
                    description=data["desc"],
                    quantity=data["qty"],
                    unit_price_minor=data["price"],
                    discount_minor=0,
                    line_total_minor=data["price"] * data["qty"],
                    gst_rate_bps=1800,
                    gst_rate_name="GST 18%",
                    hsn_sac="998313",
                    gst_tax_minor=tax_amt,
                    gst_cgst_minor=cgst,
                    gst_sgst_minor=sgst,
                    gst_igst_minor=0,
                    sort_order=0
                )

                if data.get("is_paid"):
                    pmt = Payment.objects.create(
                        organization=org,
                        customer=data["cust"],
                        amount_minor=inv.total_minor,
                        currency="INR",
                        payment_date=data["inv_date"] + timedelta(days=10),
                        reference="NEFT-DEMO-998877",
                        notes="Full payment settled via NEFT",
                        created_by=user,
                    )
                    PaymentAllocation.objects.create(
                        payment=pmt,
                        invoice=inv,
                        amount_minor=inv.total_minor,
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded {created_count} demo invoices, 3 customers, and products for '{org.name}'!"
        ))


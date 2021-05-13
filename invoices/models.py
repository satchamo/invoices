from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.template.loader import render_to_string

from . import patches  # noqa

support_email = getattr(settings, "INVOICE_EMAIL", "support@aptibyte.com")

class Manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using("invoice")


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fk = models.CharField(max_length=255)
    charge_id = models.CharField(max_length=255)
    card = models.CharField(max_length=255)
    app = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    customer = models.CharField(max_length=255, default="")
    reference_number = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")

    objects = Manager()

    class Meta:
        db_table = "invoice"
        ordering = ['created_on']
        managed = False

    @classmethod
    def get_available_id(cls):
        try:
            with transaction.atomic(using="invoice"):
                invoice = Invoice.create(
                    tax=0,
                    fk="",
                    charge_id="",
                    card="",
                    status="PENDING",
                    ip_address="",
                    items=[],
                )
                invoice_id = invoice.pk
                raise ValueError()
        except ValueError:
            pass

        return invoice_id

    @classmethod
    def create(cls, items, **kwargs):
        kwargs['app'] = kwargs.get("app", settings.INVOICE_APP_NAME)
        invoice = cls(**kwargs)
        invoice.save(force_insert=True)

        for item in items:
            item.invoice = invoice
            item.save()

        return invoice

    def save(self, *args, using="invoice", **kwargs):
        return super().save(*args, using=using, **kwargs)

    @property
    def subtotal(self):
        items = InvoiceItem.objects.filter(invoice=self)
        subtotal = Decimal("0.00")
        for item in items:
            subtotal += item.quantity * item.unit_price

        return subtotal

    @property
    def total(self):
        return self.subtotal + self.tax

    def customer_info(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.filter(pk=self.fk).first()
        if user:
            return user.first_name + " " + user.last_name + "\n" + user.email

        return ""

    def split_customer(self):
        customer = [line.strip() for line in self.customer.split("\n")]
        lines = []
        rest = []
        l = lines
        for line in customer:
            if line == "":
                l = rest
            else:
                l.append(line)

        return lines, rest

    def pretty_status(self):
        status = "Unpaid"
        if self.status == "PAID":
            status = "PAID"
        elif self.card[:5].lower() == "check":
            status = f"Mailed ({self.card.replace('-', ' #')})"
        return status

    def __str__(self):
        items = InvoiceItem.objects.filter(invoice=self)
        return render_to_string("invoices/invoice.txt", {
            "invoice": self,
            "items": items,
            "support_email": support_email
        })


class InvoiceItem(models.Model):
    invoice_item_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    taxable = models.BooleanField(default=True)
    # price_id from Stripe API
    price_id = models.CharField(max_length=255, default="")

    objects = Manager()

    class Meta:
        db_table = "invoice_item"
        managed = False

    @property
    def total(self):
        return self.quantity * self.unit_price

    def save(self, *args, using="invoice", **kwargs):
        return super().save(*args, using=using, **kwargs)

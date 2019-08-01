from decimal import Decimal

from django.conf import settings
from django.db import models
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

    objects = Manager()

    class Meta:
        db_table = "invoice"
        ordering = ['created_on']
        managed = False

    @classmethod
    def create(cls, items, **kwargs):
        kwargs['app'] = settings.INVOICE_APP_NAME
        invoice = cls(**kwargs)
        invoice.save()

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

    objects = Manager()

    class Meta:
        db_table = "invoice_item"
        managed = False

    @property
    def total(self):
        return self.quantity * self.unit_price

    def save(self, *args, using="invoice", **kwargs):
        return super().save(*args, using=using, **kwargs)

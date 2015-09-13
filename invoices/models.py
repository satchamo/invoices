from django.db import models
from decimal import Decimal
from django.template.loader import render_to_string
from django.conf import settings


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fk = models.CharField(max_length=255)
    charge_id = models.CharField(max_length=255)
    card = models.CharField(max_length=255)
    app = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    class Meta:
        db_table = "invoice"
        ordering = ['created_on']
        managed = False

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
        return render_to_string("invoices/invoice.txt", {"invoice": self, "items": items})

    @classmethod
    def create(cls, items, **kwargs):
        kwargs['app'] = settings.INVOICE_APP_NAME
        invoice = cls(**kwargs)
        invoice.save()

        for item in items:
            item.invoice = invoice
            item.save()

        return invoice

class InvoiceItem(models.Model):
    invoice_item_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    taxable = models.BooleanField(default=True)

    @property
    def total(self):
        return self.quantity * self.unit_price

    class Meta:
        db_table = "invoice_item"
        managed = False

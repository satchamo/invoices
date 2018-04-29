from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Invoice, InvoiceItem, support_email

app = settings.INVOICE_APP_NAME
get_fk_from_request = getattr(settings, "INVOICE_GET_FK_FROM_REQUEST", lambda request: request.user.pk)


@login_required
def list_(request):
    invoices = Invoice.objects.filter(app=app, fk=get_fk_from_request(request))

    return render(request, "invoices/list.html", {
        "invoices": invoices,
    })


@login_required
def detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, app=app, fk=get_fk_from_request(request))
    items = InvoiceItem.objects.filter(invoice=invoice)
    logo_url = getattr(settings, "INVOICE_LOGO_URL", None)

    return render(request, "invoices/print.html", {
        "invoice": invoice,
        "items": items,
        "request": request,
        "logo_url": logo_url,
        "support_email": support_email,
    })

from django import template
from django.template.defaultfilters import stringfilter
from ..models import Invoice

register = template.Library()

@register.filter
def has_invoices(user):
    return Invoice.objects.filter(fk=user.pk).count() > 0

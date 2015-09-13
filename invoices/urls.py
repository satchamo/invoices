from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^list/?$', views.list_, name="invoices-list"),
    url(r'^detail/(\d+)/?$', views.detail, name="invoices-detail"),
)


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/?$', views.list_, name="invoices-list"),
    url(r'^detail/(\d+)/?$', views.detail, name="invoices-detail"),
]

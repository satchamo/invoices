from django.conf.urls import include, url

urlpatterns = [
    # we just need a dummy view to do something
    url(r'^invoices/', include('invoices.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls'))
]

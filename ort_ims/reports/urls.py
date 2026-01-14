from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

app_name = "reports"
urlpatterns = [
    path("amz", views.amz_report, name="amz_report"),
    path("burn", views.burn_report, name="burn_report"),
    path("emc", views.emc_report, name="emc_report"),
    path("harmonic", views.harmonic_report, name="harmonic_report"),
]
urlpatterns += staticfiles_urlpatterns()

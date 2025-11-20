from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = "ortreports"
urlpatterns = []
urlpatterns += staticfiles_urlpatterns()

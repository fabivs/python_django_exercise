from django.urls import path

from . import views

urlpatterns = [
    # TODO: make sure that we are REST compliant
    path("reports/", views.get_reports),
]
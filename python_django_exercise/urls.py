from django.urls import include, path
from rest_framework import routers

from reports import views

urlpatterns = [path("api/v1/reports/", views.ListReportsView.as_view())]

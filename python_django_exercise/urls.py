from django.urls import include, path
from rest_framework import routers

from reports import views

router = routers.DefaultRouter()
router.register(r"reports", views.ReportViewSet)

urlpatterns = [path("api/v1/", include(router.urls))]

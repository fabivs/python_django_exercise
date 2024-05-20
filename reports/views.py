from rest_framework import viewsets
from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reports to be viewed.
    """

    queryset = Report.objects.all().order_by("id")
    serializer_class = ReportSerializer

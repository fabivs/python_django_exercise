from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer


class ListReportsView(APIView):
    def get(self, request, format=None):
        """
        Return a list of all reports.
        """

        reports = Report.objects.all().order_by("id")
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)

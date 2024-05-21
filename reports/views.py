from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from django_filters import rest_framework as filters


class ReportFilter(filters.FilterSet):
    restaurant = filters.CharFilter(lookup_expr="exact")

    class Meta:
        model = Report
        fields = ["restaurant"]


class ListReportsView(ListAPIView):
    queryset = Report.objects.all().order_by("id")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ReportFilter

    def get(self, request, format=None):
        """
        Return a list of all reports.
        """

        filtered_reports = self.filter_queryset(self.queryset)
        serializer = ReportSerializer(filtered_reports, many=True)
        return Response(serializer.data)

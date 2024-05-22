from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer
from django_filters import rest_framework as filters
from django.db.models import Sum


class ReportFilter(filters.FilterSet):
    restaurant = filters.CharFilter(lookup_expr="exact")
    date__gte = filters.DateFilter(field_name="date", lookup_expr="gte")
    date__lte = filters.DateFilter(field_name="date", lookup_expr="lte")

    sort_by = filters.OrderingFilter(
        fields=(
            ("date", "date"),
            ("restaurant", "restaurant"),
            ("planned_hours", "planned_hours"),
            ("actual_hours", "actual_hours"),
            ("budget", "budget"),
            ("sells", "sells"),
            ("planned_actual_hours_difference", "planned_actual_hours_difference"),
            ("budget_sells_difference", "budget_sells_difference"),
        ),
    )

    class Meta:
        model = Report
        fields = ["restaurant"]


class ListReportsView(ListAPIView):
    queryset = Report.objects.all().order_by("id")
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ReportFilter
    ordering_fields = [
        "planned_hours",
        "actual_hours",
        "budget",
        "sells",
        "planned_actual_hours_difference",
        "budget_sells_difference",
    ]

    def get(self, request, format=None):
        """
        Return a list of all reports.
        """

        filtered_reports = self.filter_queryset(self.queryset)
        serializer = ReportSerializer(filtered_reports, many=True)
        return Response(serializer.data)


class AggregateReportFilter(filters.FilterSet):
    restaurant = filters.CharFilter(lookup_expr="exact")
    date = filters.DateFilter(lookup_expr="exact")

    class Meta:
        model = Report
        fields = ["restaurant", "date"]


class AggregateReportView(ListAPIView):
    queryset = Report.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AggregateReportFilter

    def get(self, request):
        """
        Given a date or a restaurant name, return an aggregate report.
        The aggregate report contains the sum of all the values from
        the obtained reports.
        """

        restaurant = request.query_params.get("restaurant")
        date = request.query_params.get("date")
        if not (restaurant or date):
            return Response(
                {"error": "Please provide either restaurant or date"}, status=400
            )

        filtered_reports = self.filter_queryset(self.queryset)

        aggregate_report = filtered_reports.aggregate(
            total_planned_hours=Sum("planned_hours"),
            total_actual_hours=Sum("actual_hours"),
            total_budget=Sum("budget"),
            total_sells=Sum("sells"),
        )

        aggregate_report["total_planned_actual_hours_difference"] = (
            aggregate_report["total_planned_hours"]
            - aggregate_report["total_actual_hours"]
        )
        aggregate_report["total_budget_sells_difference"] = (
            aggregate_report["total_budget"] - aggregate_report["total_sells"]
        )

        return Response(aggregate_report)

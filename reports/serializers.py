from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "date",
            "restaurant",
            "planned_hours",
            "actual_hours",
            "budget",
            "sells",
            "planned_actual_hours_delta",
            "budget_sells_delta",
        ]

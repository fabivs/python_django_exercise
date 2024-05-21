from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    planned_actual_hours_difference = serializers.IntegerField()
    budget_sells_difference = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Report
        fields = [
            "date",
            "restaurant",
            "planned_hours",
            "actual_hours",
            "budget",
            "sells",
            "planned_actual_hours_difference",
            "budget_sells_difference",
        ]

from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    hours_difference = serializers.ReadOnlyField()
    budget_difference = serializers.ReadOnlyField()

    class Meta:
        model = Report
        fields = [
            "date",
            "restaurant",
            "planned_hours",
            "actual_hours",
            "budget",
            "sells",
            "hours_difference",
            "budget_difference",
        ]

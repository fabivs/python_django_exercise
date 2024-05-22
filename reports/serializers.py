from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    planned_actual_hours_delta = serializers.SerializerMethodField()
    budget_sells_delta = serializers.SerializerMethodField()

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

    def get_planned_actual_hours_delta(self, obj):
        try:
            return obj.planned_actual_hours_delta
        except:
            return None

    def get_budget_sells_delta(self, obj):
        try:
            return obj.budget_sells_delta
        except:
            return None

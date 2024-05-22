from django.test import TestCase
from rest_framework.test import APIClient
from reports.models import Report
from rest_framework import status
from datetime import date
from decimal import Decimal
import json


class TestReportAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.report = Report.objects.create(
            date=date(2023, 1, 20),
            restaurant="Restaurant test name",
            planned_hours=150,
            actual_hours=100,
            budget=Decimal("300.00"),
            sells=Decimal("500.00"),
        )

    def test_get_single_report(self):
        response = self.client.get("/api/v1/reports/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        report = response.data[0]
        self.assertEqual(report.get("date"), "2023-01-20")
        self.assertEqual(report.get("restaurant"), "Restaurant test name")
        self.assertEqual(report.get("planned_hours"), 150)
        self.assertEqual(report.get("actual_hours"), 100)
        self.assertEqual(report.get("budget"), "300.00")
        self.assertEqual(report.get("sells"), "500.00")
        self.assertEqual(report.get("planned_actual_hours_delta"), 50)
        self.assertEqual(report.get("budget_sells_delta"), "-200.00")

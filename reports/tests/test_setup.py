from django.test import TestCase
from rest_framework.test import APIClient
from reports.models import Report
from datetime import date
from decimal import Decimal


class TestReportSetup(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.report = Report.objects.bulk_create(
            [
                Report(
                    date=date(2023, 1, 20),
                    restaurant="Restaurant_A",
                    planned_hours=150,
                    actual_hours=100,
                    budget=Decimal("300.00"),
                    sells=Decimal("500.00"),
                ),
                Report(
                    date=date(2023, 4, 20),
                    restaurant="Restaurant_A",
                    planned_hours=200,
                    actual_hours=10,
                    budget=Decimal("100.00"),
                    sells=Decimal("200.00"),
                ),
                Report(
                    date=date(2024, 1, 20),
                    restaurant="Restaurant_B",
                    planned_hours=800,
                    actual_hours=900,
                    budget=Decimal("1000.00"),
                    sells=Decimal("500.00"),
                ),
                Report(
                    date=date(2023, 1, 25),
                    restaurant="Restaurant_B",
                    planned_hours=50,
                    actual_hours=80,
                    budget=Decimal("330.00"),
                    sells=Decimal("400.00"),
                ),
                Report(
                    date=date(2022, 12, 10),
                    restaurant="Restaurant_A",
                    planned_hours=234,
                    actual_hours=289,
                    budget=Decimal("819.29"),
                    sells=Decimal("711.38"),
                ),
            ]
        )

from django.test import TestCase
from data_importer.management.commands.import_reports import perform_import
from data_importer.models import Report
import csv
from decimal import Decimal

from django.db import connection
from django.test.utils import CaptureQueriesContext

test_file_path = "./test_dataset.csv"
csv_header = ["date", "restaurant", "planned_hours", "actual_hours", "budget", "sells"]


class TestImportReports(TestCase):
    def setUp(self):
        csv_lines = [
            ["2024-01-01", "First Restaurant", 141, 176, 4025.65, 2801.33],
            ["2016-12-15", "Second Restaurant", 108, 76, 2455.75, 3875.81],
            ["2016-01-01", "Third Restaurant", 30, 156, 116.99, 3967.95],
        ]

        with open(test_file_path, "w", newline="") as csv_file:
            write = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            write.writerows([csv_header] + csv_lines)

    def test_happy_path(self):
        perform_import(test_file_path)
        self.assertEqual(Report.objects.count(), 3)

        first_report = Report.objects.get(restaurant="First Restaurant")
        self.assertEqual(first_report.date.isoformat(), "2024-01-01")
        self.assertEqual(first_report.planned_hours, 141)
        self.assertEqual(first_report.actual_hours, 176)
        self.assertEqual(first_report.budget, Decimal("4025.65"))
        self.assertEqual(first_report.sells, Decimal("2801.33"))


# test with invalid filename

# test_import_reports_with_invalid_data

# use self.assertRaises(CommandError)

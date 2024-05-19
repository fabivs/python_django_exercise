from django.test import TestCase
from django.core.management.base import CommandError
from data_importer.management.commands.import_reports import execute
from data_importer.models import Report
import csv
from decimal import Decimal
import os

test_file_path = "./test_dataset.csv"


class TestImportReports(TestCase):
    def setUp(self):
        csv_lines = [
            ["2024-01-01", "First Restaurant", 141, 176, 4025.65, 2801.33],
            ["2016-12-15", "Second Restaurant", 108, 76, 2455.75, 3875.81],
            ["2016-01-01", "Third Restaurant", 30, 156, 116.99, 3967.95],
        ]

        _write_test_csv_file(csv_lines)

    def tearDown(self) -> None:
        os.remove(test_file_path)
        return super().tearDown()

    def test_import_reports_happy_path(self):
        execute(test_file_path)
        self.assertEqual(Report.objects.count(), 3)

        first_report = Report.objects.get(restaurant="First Restaurant")
        self.assertEqual(first_report.date.isoformat(), "2024-01-01")
        self.assertEqual(first_report.planned_hours, 141)
        self.assertEqual(first_report.actual_hours, 176)
        self.assertEqual(first_report.budget, Decimal("4025.65"))
        self.assertEqual(first_report.sells, Decimal("2801.33"))


class TestImportReportsErrors(TestCase):
    def tearDown(self) -> None:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
        return super().tearDown()

    def test_import_reports_file_not_found(self):
        with self.assertRaisesMessage(
            CommandError, "File ./just_a_random_file_path.csv does not exist"
        ):
            execute("./just_a_random_file_path.csv")

    def test_import_reports_with_invalid_date(self):
        invalid_csv_line = ["Not-a-date", "Name", 141, 176, 4025.65, 2801.33]
        _write_test_csv_file([invalid_csv_line])
        with self.assertRaisesMessage(CommandError, "Invalid data in csv at row 2"):
            execute(test_file_path)

    def test_import_reports_with_invalid_hours(self):
        invalid_csv_line = ["2024-01-01", "Name", "Not an int", 176, 4025.65, 2801.33]
        _write_test_csv_file([invalid_csv_line])
        with self.assertRaisesMessage(CommandError, "Invalid data in csv at row 2"):
            execute(test_file_path)

    def test_import_reports_with_invalid_budget(self):
        invalid_csv_line = ["2024-01-01", "Name", 141, 176, "Not a decimal", 2801.33]
        _write_test_csv_file([invalid_csv_line])
        with self.assertRaisesMessage(CommandError, "Invalid data in csv at row 2"):
            execute(test_file_path)


def _write_test_csv_file(csv_lines):
    csv_header = [
        "date",
        "restaurant",
        "planned_hours",
        "actual_hours",
        "budget",
        "sells",
    ]
    with open(test_file_path, "w", newline="") as csv_file:
        write = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        write.writerows([csv_header] + csv_lines)

from django.core.management.base import BaseCommand, CommandError
import csv
from datetime import datetime
from data_importer.models import Report


class Command(BaseCommand):
    help = "Imports the reports data from a csv dataset"

    def add_arguments(self, parser):
        parser.add_argument("--filename", type=str, required=True)

    def handle(self, *args, **options):
        filename = options["filename"]
        imported_records_count = import_reports(filename)
        self.stdout.write(
            self.style.SUCCESS(
                f"Reports successfully imported {imported_records_count} records from {filename}!"
            )
        )


def import_reports(filename):
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        imported_records_count = 0

        for row in reader:
            Report.objects.create(
                date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                restaurant=row["restaurant"],
                planned_hours=row["planned_hours"],
                actual_hours=row["actual_hours"],
                budget=row["budget"],
                sells=row["sells"],
            )
            imported_records_count += 1

    return imported_records_count
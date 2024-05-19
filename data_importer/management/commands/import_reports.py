from django.core.management.base import BaseCommand, CommandError
import csv
from datetime import datetime
from data_importer.models import Report


class Command(BaseCommand):
    help = "Imports the reports data from a csv dataset"

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, nargs='?', default="dataset.csv")

    def handle(self, *args, **options):
        filename = options["filename"]
        self.stdout.write(self.style.SUCCESS(
            f"Importing records from {filename}..."))
        imported_counter = import_reports(filename)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {imported_counter} records.")
        )


def import_reports(filename):
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        imported_counter = 0
        for row in reader:
            Report.objects.create(
                date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                restaurant=row["restaurant"],
                planned_hours=row["planned_hours"],
                actual_hours=row["actual_hours"],
                budget=row["budget"],
                sells=row["sells"],
            )
            imported_counter += 1

    return imported_counter

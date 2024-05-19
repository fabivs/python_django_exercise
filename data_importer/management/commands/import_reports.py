from django.core.management.base import BaseCommand, CommandError
import csv
from datetime import datetime
from data_importer.models import Report
import os


class Command(BaseCommand):
    help = "Imports the reports data from a csv dataset"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, nargs="?", default="dataset.csv")

    def handle(self, *args, **options):
        filepath = options["filepath"]
        self.stdout.write(self.style.SUCCESS(f"Importing records from {filepath}..."))
        imported_counter = execute(filepath)
        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {imported_counter} records.")
        )


def execute(filepath):
    if not os.path.exists(filepath):
        raise CommandError(f"File {filepath} does not exist")
    with open(filepath, "r") as file:
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

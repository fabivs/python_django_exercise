from django.core.management.base import BaseCommand, CommandError
import csv
from datetime import datetime
from data_importer.models import Report
import os
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Imports the reports data from a csv dataset"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, nargs="?", default="dataset.csv")

    def handle(self, *args, **options):
        filepath = options["filepath"]
        self.stdout.write(self.style.SUCCESS(f"Importing records from {filepath}..."))
        imported_count = execute(filepath)
        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {imported_count} records.")
        )


def execute(filepath):
    if not os.path.exists(filepath):
        raise CommandError(f"File {filepath} does not exist")

    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                Report.objects.create(
                    date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                    restaurant=row["restaurant"],
                    planned_hours=row["planned_hours"],
                    actual_hours=row["actual_hours"],
                    budget=row["budget"],
                    sells=row["sells"],
                )
            except (ValueError, ValidationError):
                raise CommandError(f"Invalid data in csv at row {reader.line_num}")

    return reader.line_num - 1

from django.db import models
from django.db.models import F


class Report(models.Model):
    date = models.DateField()
    restaurant = models.CharField(max_length=100)
    planned_hours = models.IntegerField()
    actual_hours = models.IntegerField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    sells = models.DecimalField(max_digits=10, decimal_places=2)
    planned_actual_hours_delta = models.GeneratedField(
        expression=F("planned_hours") - F("actual_hours"),
        output_field=models.IntegerField(),
        db_persist=True,
    )
    budget_sells_delta = models.GeneratedField(
        expression=F("budget") - F("sells"),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
    )

from django.db import models


class Report(models.Model):
    date = models.DateField()
    restaurant = models.CharField(max_length=100)
    planned_hours = models.IntegerField()
    actual_hours = models.IntegerField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    sells = models.DecimalField(max_digits=10, decimal_places=2)

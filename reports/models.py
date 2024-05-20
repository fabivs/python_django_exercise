from django.db import models


class Report(models.Model):
    date = models.DateField()
    restaurant = models.CharField(max_length=100)
    planned_hours = models.IntegerField()
    actual_hours = models.IntegerField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    sells = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def hours_difference(self):
        return self.planned_hours - self.actual_hours

    @property
    def budget_difference(self):
        return self.budget - self.sells

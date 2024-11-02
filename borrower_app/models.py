from django.db import models


class BorrowerInfo(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    item_quantity = models.IntegerField()
    date_borrowed = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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


class ReturnedItem(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    item_quantity = models.PositiveIntegerField()
    date_borrowed = models.DateField()
    date_returned = models.DateField(auto_now_add=True)  # Automatically set the date when returned

    def __str__(self):
        return f"{self.last_name}, {self.first_name} - {self.item_name} (Returned)"

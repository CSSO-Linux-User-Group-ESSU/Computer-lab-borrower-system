from django.db import models


# Create your models here.
class BorrowerInfo(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    projector_qty = models.IntegerField(max_length=5)
    led_qty = models.IntegerField(max_length=5)
    monitor_qty = models.IntegerField(max_length=5)
    keyboard_qty = models.IntegerField(max_length=5)
    mouse_qty = models.IntegerField(max_length=5)
    cpu_qty = models.IntegerField(max_length=5)
    ups_qty = models.IntegerField(max_length=5)
    sub_cord_qty = models.IntegerField(max_length=5)
    power_cord_qty = models.IntegerField(max_length=5)

    def __str__(self):
        return f" Borrower {self.last_name}, {self.first_name} {self.middle_name}."

    def total_quantity(self):
        return (self.led_qty +
                self.monitor_qty +
                self.keyboard_qty +
                self.mouse_qty +
                self.cpu_qty +
                self.ups_qty +
                self.sub_cord_qty)



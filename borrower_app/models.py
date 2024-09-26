from django.db import models


# Create your models here.
class BorrowerInfo(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    middle_initial = models.CharField(max_length=3)
    projector_qty = models.CharField(max_length=5)
    led_qty = models.CharField(max_length=5)
    monitor_qty = models.CharField(max_length=5)
    keyboard_qty = models.CharField(max_length=5)
    mouse_qty = models.CharField(max_length=5)
    cpu_qty = models.CharField(max_length=5)
    ups_qty = models.CharField(max_length=5)
    sub_cord_qty = models.CharField(max_length=5)
    power_cord_qty = models.CharField(max_length=5)
    total_qty = models.CharField(max_length=5)
    other_qty = models.CharField(max_length=20)


    def __str__(self):
        pass




from django.db import models

class BorrowerInfo(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True, null=True)  # Optional field
    projector_qty = models.PositiveIntegerField(default=0)
    led_qty = models.PositiveIntegerField(default=0)
    monitor_qty = models.PositiveIntegerField(default=0)
    keyboard_qty = models.PositiveIntegerField(default=0)
    mouse_qty = models.PositiveIntegerField(default=0)
    cpu_qty = models.PositiveIntegerField(default=0)
    ups_qty = models.PositiveIntegerField(default=0)
    sub_cord_qty = models.PositiveIntegerField(default=0)
    power_cord_qty = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Borrower {self.last_name}, {self.first_name} {self.middle_name}."

    def total_quantity(self):
        return (self.led_qty +
                self.monitor_qty +
                self.keyboard_qty +
                self.mouse_qty +
                self.cpu_qty +
                self.ups_qty +
                self.sub_cord_qty +
                self.power_cord_qty +  # Ensure to include all relevant fields
                self.projector_qty)  # Include projector_qty as well


class ReturnedItem(models.Model):
    borrower = models.ForeignKey(BorrowerInfo, on_delete=models.CASCADE)  # Reference to the original borrower
    returned_date = models.DateTimeField(auto_now_add=True)  # Store the date when the item was returned
    projector_qty = models.PositiveIntegerField(default=0)
    led_qty = models.PositiveIntegerField(default=0)
    monitor_qty = models.PositiveIntegerField(default=0)
    keyboard_qty = models.PositiveIntegerField(default=0)
    mouse_qty = models.PositiveIntegerField(default=0)
    cpu_qty = models.PositiveIntegerField(default=0)
    ups_qty = models.PositiveIntegerField(default=0)
    sub_cord_qty = models.PositiveIntegerField(default=0)
    power_cord_qty = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Returned Items of {self.borrower.last_name}, {self.borrower.first_name} on {self.returned_date.strftime('%Y-%m-%d')}."

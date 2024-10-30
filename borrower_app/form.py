from django import forms
from .models import BorrowerInfo


class UploadFileForm(forms.Form):
    files = forms.FileField()


class BorrowerForm(forms.ModelForm):
    class Meta:
        model = BorrowerInfo
        fields = [
            'last_name',
            'first_name',
            'middle_name',
            'projector_qty',
            'led_qty',
            'monitor_qty',
            'keyboard_qty',
            'mouse_qty',
            'cpu_qty',
            'ups_qty',
            'sub_cord_qty',
            'power_cord_qty',
            'date'
        ]

        labels = {
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'projector_qty': 'Projector Quantity',
            'led_qty': 'LED Quantity',
            'monitor_qty': 'Monitor Quantity',
            'keyboard_qty': 'Keyboard Quantity',
            'mouse_qty': 'Mouse Quantity',
            'cpu_qty': ' CPU Quantity',
            'ups_qty': 'UPS Quantity',
            'sub_cord_qty': 'Sub Chord Quantity',
            'power_cord_qty': 'Power Chord Quantity',
            'date': 'Date'
        }


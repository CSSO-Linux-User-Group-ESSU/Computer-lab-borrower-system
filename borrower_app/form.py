from django import forms
from .models import BorrowerInfo


class BorrowerForm(forms.ModelForm):
    class Meta:
        model = BorrowerInfo
        fields = [
            'last_name',
            'first_name',
            'middle_name',
            'item_name',
            'item_quantity'
        ]
        labels = {
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'middle_name': 'Middle Name',
            'item_name': 'Item Name',
            'item_quantity': 'Item Quantity'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_quantity'].widget.attrs.update({'min': 0})  # Ensure non-negative value

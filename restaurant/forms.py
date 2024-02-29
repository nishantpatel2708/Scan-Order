from django import forms
from .models import *


class ParcelOrderItemForm(forms.ModelForm):
    class Meta:
        model = Parcel_OrderItem
        fields = [
            'product', 'quantity'
        ]

        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
            }),
            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }
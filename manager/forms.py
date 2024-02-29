from django import forms
from .models import *
from accounts.models import User
from restaurant.models import *


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Parcel_Customer
        fields = [
            'name', 'mobile_no',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
            })

        }
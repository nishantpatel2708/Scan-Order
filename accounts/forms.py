from django import forms
from .models import *


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password',
            'restaurant_name', 'mobile_no', 'address', 'country', 'state',
            'pin_code', 'land_line_number', 'discount', 'offer', 'GST_Number',
            'SGST', 'CGST', 'profile_photo'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'restaurant_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'mobile_no': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'pin_code': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'land_line_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'discount': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'offer': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'GST_Number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'SGST': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'CGST': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': '',
            })
        }

from django import forms
from .models import *
from accounts.models import User
from restaurant.models import OrderItem


class QrForm(forms.ModelForm):
    table_no = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Table
        fields = ['table_no']


class AddMenuForm(forms.ModelForm):

    class Meta:
        model = MenuTable
        exclude = ['res', 'status']
        widgets = {
            'Dish_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Dish_Description': forms.TextInput(attrs={'class': 'form-control'}),
            'speciality': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Price': forms.TextInput(attrs={'class': 'form-control'}),
            'pices': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'Dish_image': forms.FileInput(attrs={'class': 'form-control'}),
            }

    def __init__(self, user, *args, **kwargs):
        super(AddMenuForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Categories.objects.filter(
            rest_id=user)


class AddCategoryForm(forms.ModelForm):
    Category_Name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))

    Description = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))

    Category_Image = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
        }))
    class Meta:
        model = Categories
        fields = '__all__'
        exclude = ['rest']
        widgets = {
            'Category_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': forms.TextInput(attrs={'class': 'form-control'}),
            'Category_Image': forms.FileInput(attrs={'class': 'form-control'}),
            }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password',
            'mobile_no', 'address', 'country', 'state', 'pin_code',
            'Adhaar_Card', 'Category', 'salary', 'profile_photo'
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
            'Adhaar_Card': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'Category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'salary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': 'form-control',
            })
        }


class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'mobile_no', 'address', 'country', 'state', 'pin_code',
            'Adhaar_Card', 'Category', 'salary', 'profile_photo'
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
            'Adhaar_Card': forms.FileInput(attrs={
                'class': '',
            }),
            'Category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'salary': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': '',
            })
        }


class ComForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = OrderItem
        fields = ['comment']


class ExpensesForm(forms.ModelForm):
    
    class Meta:
        model = Expenses
        fields = '__all__'
        exclude = ('res', )

        widgets = {
            'Day_Expense': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Date': forms.DateTimeInput(attrs={
                'class': 'form-control ',
                'type': 'datetime-local'
            }),
            'Others': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

class EditExpensesForm(forms.ModelForm):
    
    class Meta:
        model = Expenses
        fields = '__all__'
        exclude = ('res', 'Date')

        widgets = {
            'Day_Expense': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'Others': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class PerMonthExpensesForm(forms.ModelForm):
    
    class Meta:
        model = PerMonthExpenses
        fields = '__all__'
        exclude = ('res', )
        widgets = {
            'Rent': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Light_Bill': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Others': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Date': forms.DateTimeInput(attrs={
                'class': 'form-control ',
                'type': 'datetime-local'
            }),
        }


class EditMonthExpensesForm(forms.ModelForm):
    
    class Meta:
        model = PerMonthExpenses
        fields = '__all__'
        exclude = ('res', 'Date')

        widgets = {
            'Rent': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Light_Bill': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Others': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }



class AssestsForm(forms.ModelForm):
    
    class Meta:
        model = Assests
        fields = '__all__'
        exclude = ('res', )
        widgets = {
            'Furnishing': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Kitchen_equipements': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Others': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'Date': forms.DateTimeInput(attrs={
                'class': 'form-control ',
                'type': 'datetime-local'
            }),
        }


class AddUnitForm(forms.ModelForm):
    unit_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))


    class Meta:
        model = Unit
        fields = '__all__'
        exclude = ['rest']



class AddInventoryForm(forms.ModelForm):

    Item_Name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    Item_Amount = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    Item_Price = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
        }))


    class Meta:
        model = Inventory
        exclude = ['rest', 'Date']
        widgets = {'Unit': forms.Select(attrs={'class': 'form-control'})}

    def __init__(self, user, *args, **kwargs):
        super(AddInventoryForm, self).__init__(*args, **kwargs)
        self.fields['Unit'].queryset = Unit.objects.filter(
            rest_id=user)
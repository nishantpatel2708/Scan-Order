from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.

e_category = (('waiter', 'waiter'), ('manager', 'manager'), ('chef', 'chef'),
                ('d_boy', 'delivery boy'))


class User(AbstractUser):

    mobile_no = models.CharField(max_length=10,
                                    validators=[RegexValidator(r'^\d{9,10}$')])
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=6,
                                validators=[RegexValidator(r'^\d{5,6}$')])
    profile_photo = models.ImageField(upload_to='profile_pic',
                                        null=True,
                                        blank=True)

    restaurant_name = models.CharField(max_length=120, null=True, blank=True)
    land_line_number = models.CharField(
        max_length=6,
        validators=[RegexValidator(r'^\d{5,6}$')],
        null=True,
        blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    offer = models.CharField(max_length=10, null=True, blank=True)
    GST_Number = models.CharField(max_length=30, null=True, blank=True)
    SGST = models.CharField(max_length=6, null=True, blank=True)
    CGST = models.CharField(max_length=6, null=True, blank=True)

    rest = models.ForeignKey('self',
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    Adhaar_Card = models.FileField(upload_to='emp_det', null=True, blank=True)
    Category = models.CharField(choices=e_category,
                                max_length=10,
                                null=True,
                                blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    is_rest = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
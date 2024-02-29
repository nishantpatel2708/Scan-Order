from django.contrib.auth.models import User
from rest_admin.models import *
from django.core.validators import RegexValidator
from django.db import models
from rest_admin.models import *


class OrderItem(models.Model):
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(
        MenuTable, on_delete=models.CASCADE, related_name='product')
    quantity = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=120, blank=True, null=True)   
    table_no = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='table_id')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=30, default='pending')

    def __str__(self):
        return f"{self.quantity} of {self.product.Dish_Name}"

    def get_total_item_price(self):
        return self.quantity * self.product.Price


class Order(models.Model):
    table_no = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='order_table_id')
    item = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    comment = models.CharField(max_length=120, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=100)
    total_bill = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.table_no.rest.restaurant_name

    def get_total(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        return total

    def sgst_price(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        sgst = (total * int(self.table_no.rest.SGST)) / 100
        return sgst

    def cgst_price(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        cgst = (total * int(self.table_no.rest.SGST)) / 100
        return cgst

    def sc_total(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        gst = (total*int(self.table_no.rest.SGST))/100
        cgst = (total*int(self.table_no.rest.CGST))/100
        net_price = total+gst+cgst

        return round(net_price)


    def gst_total(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        gst = (total*int(self.table_no.rest.SGST))/100
        cgst = (total*int(self.table_no.rest.CGST))/100

        t = total + gst + cgst

        if self.table_no.rest.discount != 0:
            t -= self.table_no.rest.discount
        

        if t < 0:
            t = 0
        else:
            t = t
        return round(t)


class Parcel_Customer(models.Model):
    rest = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=True, null=True)
    mobile_no = models.CharField(max_length=10,
                                 validators=[RegexValidator(r'^\d{9,10}$')])


class Parcel_OrderItem(models.Model):
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(
        MenuTable, on_delete=models.CASCADE, related_name='parcel_product')
    quantity = models.PositiveIntegerField(default=1)
    comment = models.CharField(max_length=120, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=30, default='pending')
    customer = models.ForeignKey(
        Parcel_Customer, on_delete=models.CASCADE, related_name='username')

    def __str__(self):
        return f"{self.quantity} of {self.product.Dish_Name}"

    def get_total_item_price(self):
        return self.quantity * self.product.Price


class Parcel_Order(models.Model):
    item = models.ManyToManyField(Parcel_OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    comment = models.CharField(max_length=120, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    status = models.CharField(max_length=100)
    total_bill = models.IntegerField(null=True, blank=True)
    customer = models.ForeignKey(
        Parcel_Customer, on_delete=models.CASCADE, related_name='Order_username')


    def get_total(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        return total

    def sgst_price(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        sgst = (total * int(self.customer.rest.SGST)) / 100
        return sgst

    def cgst_price(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        cgst = (total * int(self.customer.rest.SGST)) / 100
        return cgst

    def sc_total(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        gst = (total*int(self.customer.rest.SGST))/100
        cgst = (total*int(self.customer.rest.CGST))/100
        net_price = total+gst+cgst

        return round(net_price)

    def gst_total(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()

        if self.customer.rest.discount != 0:
            total -= self.customer.rest.discount

        gst = (total*int(self.customer.rest.SGST))/100
        cgst = (total*int(self.customer.rest.CGST))/100
        net_price = total+gst+cgst
        if net_price < 0:
            net_price = 0
        else:
            net_price = net_price
        return round(net_price)


# create a table for waiter Call store the data. Create A signal For this model using post save and then send the message as payload to the group
from django.db.models.signals import post_save
from channels.layers import get_channel_layer 
from asgiref.sync import async_to_sync
from django.dispatch import receiver
import json
class CallWaiter(models.Model):
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='call_waiter')
    Status = models.BooleanField(default=False)

@receiver(post_save, sender=CallWaiter)
def call_waiter_handler(sender, instance, created, **kwargs):
    print('demo')
    print(created)
    if created:
        channael_layer = get_channel_layer()
        data = {}
        data['rest'] = instance.table.rest_id

        data['message'] = 'Table No. {} calling waiter'.format(instance.table.id)
        
        async_to_sync(channael_layer.group_send)(
            'waiter_call_%s' % instance.table.rest_id, {
                'type': 'call_wait',
                'value': json.dumps(data)
            }
        )
    
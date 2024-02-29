from django.forms.widgets import CheckboxInput
from django.shortcuts import render, HttpResponse
from django.template.loader import get_template
from rest_admin.utils import render_to_pdf
from django.views.generic import View
from django.http import HttpResponse
import datetime
from restaurant.forms import *
from django.contrib import messages

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse
from rest_admin.models import *
from rest_admin.forms import *
from accounts.models import User
from restaurant.models import *
from django.utils import timezone
from django.forms import fields, formset_factory, modelformset_factory
from .forms import *

# Create your views here.

def qr(request):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    if request.method == 'POST':
        form = QrForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.rest = res
            form_r.status = 'available'
            form_r.save()
            return redirect('manager:table_list')
        else:
            print(form.errors)
    else:
        form = QrForm()
    return render(request, 'manager/index.html', {
        'form': form,
        'restro': restro
    })



def add_menu(request):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    if request.method == 'POST':
        form = AddMenuForm(res.id, request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.res = res
            form_r.status = 'available'
            form_r.save()
            return redirect('manager:menu_list')
        else:
            print(form.errors)
    else:
        form = AddMenuForm(res.id)
    return render(request, 'manager/add_menu.html', {
        'form': form,
        'restro': restro
    })


def add_categories(request):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.rest = res
            form_r.save()
            return redirect('manager:cat_list')
        else:
            print(form.errors)
    else:
        form = AddCategoryForm()
    return render(request, 'manager/add_category.html', {
        'form': form,
        'restro': restro
    })


def category_list(request):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    cat_list = Categories.objects.filter(rest_id=res)
    return render(request, 'manager/cat_list.html', {
        'cat_list': cat_list,
        'restro': restro
    })


def menu_list(request):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    menu_lists = MenuTable.objects.filter(res_id=res)
    return render(request, 'manager/menu_list.html', {
        'menu_lists': menu_lists,
        'restro': restro
    })


def cat_form_edit(request, id):
    restro = User.objects.get(id=request.user.rest_id)
    
    instance = get_object_or_404(Categories, id=id)

    form = AddCategoryForm(request.POST or None,request.FILES or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('manager:cat_list')
    return render(request, 'manager/cat_edit.html', {
        'form': form,
        'restro': restro
    })


def delete(request, id):
    user2 = Categories.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('manager:cat_list'))

def menu_form_edit(request, id):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    instance = get_object_or_404(MenuTable, id=id)

    form = AddMenuForm(res, request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('manager:menu_list')
    return render(request, 'manager/edit_menu.html', {
        'form': form,
        'restro': restro
    })


def menu_delete(request, id):
    user2 = MenuTable.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('manager:menu_list'))


def menu_avc(request, id):
    item = MenuTable.objects.get(id=id)
    if item.status == 'available':
        item.status = 'Not Available'
        item.save()
    else:
        item.status = 'available'
        item.save()

    return HttpResponseRedirect(reverse('manager:menu_list'))


def table_view(request):
    restro = User.objects.get(id=request.user.rest_id)
    

    tables = Table.objects.filter(rest_id=request.user.rest_id)
    print(tables)
    return render(request, 'manager/tables.html', {
        'tables': tables,
        'restro': restro
    })


def table_list(request):
    restro = User.objects.get(id=request.user.rest_id)
    

    tables = Table.objects.filter(rest_id=request.user.rest_id)
    return render(request, 'manager/table_list.html', {
        'tables': tables,
        'restro': restro
    })


def table_edit(request, id):
    instance = Table.objects.get(id=id)

    form = QrForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        return redirect('manager:table_list')
    else:
        print(form.errors)
    return render(request, 'manager/table_u.html', {'form': form})


def table_delete(request, id):
    user2 = Table.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('manager:table_list'))


def orders(request):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    if request.method == 'POST':
        from_date = request.POST.get('fromDate')
        to_date = request.POST.get('toDate')
        order_list = Order.objects.filter(
            ordered_date__range=[from_date, to_date])
    else:
        order_list = Order.objects.filter(
            table_no__rest_id=res.id, ordered=True)

    return render(request, 'manager/orders.html', {'order_list': order_list, 'restro': restro})


def order_details(request, id):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    order_det = Order.objects.get(id=id)
    return render(request, 'manager/order_details.html', {'order_det': order_det, 'user': res, 'restro': restro})


def today_order(request):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    order_list = Order.objects.filter(table_no__rest_id=res.id, ordered=True,
                 ordered_date__day=datetime.datetime.today().day, status='Pending')

    parcel_order_list = Parcel_Order.objects.filter(customer__rest_id=res.id, ordered=True,
                        ordered_date__day=datetime.datetime.today().day, status='Pending')


    return render(request, 'manager/today_order.html', {'parcel_order_list':parcel_order_list, 'order_list': order_list, 'restro': restro})


def order_complete(request, id):

    o_state = Order.objects.get(id=id)
    o_state.status = 'Complete'
    o_state.save()
    table = Table.objects.get(table_no=o_state.table_no.table_no)
    table.status = 'available'
    table.save()
    return render(request, 'manager/payment.html', {'o_state': o_state})


class GeneratePdf(View):
    def get(self, request, id):
        o_state = Order.objects.get(id=id)
        o_state.status = 'Complete'
        o_state.save()
        table = Table.objects.get(table_no=o_state.table_no.table_no)
        table.status = 'available'
        table.save()
        list = Order.objects.get(id=id)

        data = {
            'bill_no': list.id,
            'sgst_amount': list.sgst_price(),
            'cgst_amount': list.cgst_price(),
            'total_gst': list.sc_total(),
            'rest_name': list.table_no.rest.restaurant_name,
            'Discount': list.table_no.rest.discount,
            'gst_number': list.table_no.rest.GST_Number,
            'rest_image': list.table_no.rest.profile_photo.url,
            'Table_No': list.table_no.table_no,
            'address': list.table_no.rest.address,
            'state': list.table_no.rest.state,
            'pin_code': list.table_no.rest.pin_code,
            'phone_no': list.table_no.rest.mobile_no,
            'Item': list.item.all(),
            'sgst': list.table_no.rest.SGST,
            'cgst': list.table_no.rest.CGST,
            'date': datetime.datetime.today().date(),
            'time': datetime.datetime.today().time(),
            'Total': list.get_total(),
            'grand_total': list.gst_total(),
        }
        pdf = render_to_pdf('manager/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


def user_details(request):
    restro = User.objects.get(id=request.user.rest_id)
    user = User.objects.get(id=request.user.id)
    return render(request, 'manager/user_profile.html', {'user': user, 'restro': restro})


def update_details(request, id):
    restro = User.objects.get(id=request.user.rest_id)
    instance = get_object_or_404(User, id=id)
    form = EditEmployeeForm(
        request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        form.save()

        return redirect('manager:user_profile')
    else:
        print(form.errors)
    return render(request, 'manager/update_u.html', {'form': form, 'restro': restro})


def com_edit(request, id):
    instance = get_object_or_404(OrderItem, id=id)

    form = ComForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        return redirect('manager:t_order')
    else:
        print(form.errors)
    return render(request, 'manager/com_u.html', {'form': form})

################## New #################
from django.forms import inlineformset_factory, Select, TextInput


def manual_order(request, id):
    restro = User.objects.get(id=request.user.rest_id)
    table = Table.objects.get(id=id)

    order_formset = inlineformset_factory(Table, OrderItem, fields=('product', 'quantity'), labels={'product': '', 'quantity': ''},
        widgets={'product': Select(attrs={'class': 'form-control', 'label': ''}),
        'quantity': TextInput(attrs={'class': 'form-control', 'size': '1'})},
        extra=1, max_num=20, can_delete=False)

    
    customer = Table.objects.get(id=id)

    formset = order_formset(
        queryset=OrderItem.objects.none(), instance=customer)

    if request.method == 'POST':

        formset = order_formset(
            request.POST, request.FILES, instance=customer)

        if formset.is_valid():
            for f in formset:
                cd = f.cleaned_data
                dish = cd.get('product')

                qua = cd.get('quantity')
            
            demo = formset.save(commit=False)

            for i in demo:
                item = get_object_or_404(MenuTable, id=i.product.id)
                
                order_qs = Order.objects.filter(
                table_no_id=id, ordered=True, status='Pending', table_no__rest=restro)
                
                if order_qs.exists():
                    order = order_qs[0]

                    if order.item.filter(product_id=item.pk, status='pending').exists() or order.item.filter(product_id=item.pk, status='Preparing'):
                        o_i = OrderItem.objects.get(product_id=i.product.id)
                        o_i.quantity += 1
                        o_i .save()
                        print('else1')
                        messages.info(request, "Item Quantity was Updated")
                        
                    else:
                        print('else2')
                        messages.info(request, "item was added to cart")
                        formset.save(commit=True)
                        order.item.add(i)
                        return redirect('manager:table_view')
                        
                else:
                    ordered_date = timezone.now()
                    print('else3')
                    order = Order.objects.create(
                        table_no_id=id, ordered_date=ordered_date,  ordered=True, status='Pending')
                    formset.save(commit=True)
                    order.item.add(i)
                    
                    messages.info(request, "item was added to cart")
        
            return redirect('manager:table_view')

        else:
            print(formset.errors)
            
    else:
        formset = order_formset()

    return render(request, 'manager/manual_order.html', {'formset': formset, 'restro': restro, 'table': table, 'id':id})

  
    
def manual_order_parcel(request):

    order_formset = inlineformset_factory(Parcel_Customer, Parcel_OrderItem, fields=('product', 'quantity'), labels={'product': '', 'quantity': ''},
    widgets={'product': Select(attrs={'class': 'form-control', 'label': ''}),
    'quantity': TextInput(attrs={'class': 'form-control', 'size': '1'})},
    extra=1, max_num=20, can_delete=False)

    customer = Parcel_Customer.objects.last()

    formset = order_formset(
        queryset=Parcel_OrderItem.objects.none(), instance=customer)

    if request.method == 'POST':

        formset = order_formset(
            request.POST, request.FILES, instance=customer)

        if formset.is_valid():
            
            demo = formset.save(commit=False)

            print("demo>>", demo)

            for i in demo:
                item = get_object_or_404(MenuTable, id=i.product.id)

                print("item>>>>>", item)
                
                order_qs = Parcel_Order.objects.filter(
                customer_id=customer.id, ordered=True, status='Pending')

                print("order_qs>>>", order_qs)

                if order_qs.exists():
                    order = order_qs[0]

                    print("order>>>", order)

                    if order.item.filter(product_id=item.pk, status='pending').exists() or order.item.filter(product_id=item.pk, status='Preparing'):
                        o_i = Parcel_OrderItem.objects.get(product_id=i.product.id)
                        o_i.quantity += 1
                        o_i .save()
                        print('else1')
                        messages.info(request, "Item Quantity was Updated")
                        
                    else:
                        print('else2')
                        messages.info(request, "item was added to cart")
                        formset.save(commit=True)
                        order.item.add(i)
                        return redirect('manager:table_view')
                        
                else:
                    ordered_date = timezone.now()
                    print('else3')
                    order = Parcel_Order.objects.create(
                        customer_id=customer.id, ordered_date=ordered_date,  ordered=True, status='Pending')
                    formset.save(commit=True)
                    order.item.add(i)
                    
                    messages.info(request, "item was added to cart")
        
            return redirect('manager:table_view')

        else:
            print(formset.errors)
            
    else:
        formset = order_formset()


    return render(request, 'manager/manual_order_parcel.html', {'customer':customer, 'formset': formset})


def add_customer(request):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)

    if request.method == 'POST':
        form = AddCustomerForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.rest = res
            form_r.save()
            return redirect('manager:manual_order_parcel')

        else:
            print(form.errors)

    else:
        form = AddCustomerForm()


    return render(request, 'manager/add_customer.html', {
        'form': form,
        'restro': restro
    })



class Parcel_GeneratePdf(View):
    def get(self, request, id):
        o_state = Parcel_Order.objects.get(id=id)
        o_state.status = 'Complete'
        o_state.save()

        customer = Parcel_Customer.objects.get(id=id)

        list = Parcel_Order.objects.get(id=id)

        data = {
            'bill_no': list.id,
            'sgst_amount': list.sgst_price(),
            'cgst_amount': list.cgst_price(),
            'total_gst': list.sc_total(),
            'rest_name': list.customer.rest.restaurant_name,
            'Discount': list.customer.rest.discount,
            'gst_number': list.customer.rest.GST_Number,
            'rest_image': list.customer.rest.profile_photo.url,
            'customer': customer.name,
            'mobile_no': customer.mobile_no,
            'address': list.customer.rest.address,
            'state': list.customer.rest.state,
            'pin_code': list.customer.rest.pin_code,
            'phone_no': list.customer.rest.mobile_no,
            'Item': list.item.all(),
            'sgst': list.customer.rest.SGST,
            'cgst': list.customer.rest.CGST,
            'date': datetime.datetime.today().date(),
            'time': datetime.datetime.today().time(),
            'Total': list.get_total(),
            'grand_total': list.gst_total(),
        }
        pdf = render_to_pdf('manager/parcel_invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
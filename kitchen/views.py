from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from accounts.models import *
from rest_admin.models import *
from restaurant.models import *
from django.shortcuts import render,redirect
import datetime
from rest_admin.forms import *

# Create your views here.


def table_view(request):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    order_list = Order.objects.filter(table_no__rest_id=res.id, ordered=True,
                                      ordered_date__day=datetime.datetime.today().day, status='Pending')
    print("order_list>>>>>", order_list)
    return render(request, 'kitchen/today_order.html', {'order_list': order_list, 'restro': restro})

def category_list(request):
    user = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.rest_id)
    cat_list = Categories.objects.filter(rest_id=user.rest_id)
    return render(request, 'kitchen/cat_list.html', {'cat_list': cat_list, 'user': user, 'res':res})


def menu_list(request):
    user = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.rest_id)
    menu_lists = MenuTable.objects.filter(res_id=res)

    return render(request, 'kitchen/menu_list.html', {'menu_lists': menu_lists, 'user': user, 'res':res})


def orders(request):
    user = User.objects.get(user_id=request.user)
    res = User.objects.get(user_id=request.user)
    order_list = Order.objects.filter(table_no__rest_id=res.rest.id, ordered=True)
    return render(request, 'kitchen/orders.html', {'order_list': order_list, 'user':user, 'res':res})


def order_details(request, id):

    res = User.objects.get(user_id=request.user)
    order_det = Order.objects.get(id=id)
    return render(request, 'kitchen/order_details.html', {'order_det': order_det, 'user': res, 'res':res})


def today_order(request):
    user = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.rest_id)
    order_list = OrderItem.objects.filter(table_no__rest_id=res.id, ordered=True,
                                          date__year=datetime.datetime.today().year,
                                          date__month=datetime.datetime.today().month,
                                          date__day=datetime.datetime.today().day)
    print(order_list)

    parcel_order_list = Parcel_OrderItem.objects.filter(customer__rest_id=res.id, ordered=True,
                                          date__year=datetime.datetime.today().year,
                                          date__month=datetime.datetime.today().month,
                                          date__day=datetime.datetime.today().day)


    return render(request, 'kitchen/today_order.html', {'parcel_order_list':parcel_order_list, 'order_list': order_list, 'res': res, 'user':user})


def status_preparing(request, id):
    o_state = OrderItem.objects.get(id=id)
    o_state.status = 'Preparing'
    o_state.save()
    return redirect('kitchen:t_order')


def status_ready_to_serve(request, id):
    o_state = OrderItem.objects.get(id=id)

    o_state.status = 'Ready To Serve'
    o_state.ordered = True
    o_state.save()
    return redirect('kitchen:t_order')


def add_menu(request):
    user = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.rest_id)
    if request.method == 'POST':
        form = AddMenuForm(res.id, request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.res = res
            form_r.status = 'available'
            form_r.save()
            return redirect('kitchen:menu_list')
        else:
            print(form.errors)
    else:
        form = AddMenuForm(res.id)
    return render(request, 'kitchen/add_menu.html', {'form': form, 'user': user, 'res':res})


def add_categories(request):
    user = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.rest_id)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.rest = res
            form_r.save()
            return redirect('kitchen:cat_list')
        else:
            print(form.errors)
    else:
        form = AddCategoryForm()
    return render(request, 'kitchen/add_category.html', {'form': form, 'user': user, 'res':res})


def user_info(request):
    user = User.objects.get(id=request.user.id)

    return render(request, 'kitchen/user_infor.html', {'i': user, 'user': user, 'res': user})


def menu_state(request, id):
    item = MenuTable.objects.get(id=id)

    if item.status == 'available':
        item.status = 'not available'
        item.save()

        return redirect('kitchen:menu_list')

    else:
        item.status = 'available'
        item.save()

        return redirect('kitchen:menu_list')
        

def parcel_status_preparing(request, id):
    o_state = Parcel_OrderItem.objects.get(id=id)
    o_state.status = 'Preparing'
    o_state.save()
    return redirect('kitchen:t_order')


def parcel_status_ready_to_serve(request, id):
    o_state = Parcel_OrderItem.objects.get(id=id)

    o_state.status = 'Ready To Serve'
    o_state.ordered = True
    o_state.save()
    return redirect('kitchen:t_order')
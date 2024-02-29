from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt 
from .forms import *
from .models import *
from accounts.models import *
from django.db.models import Sum, F
import datetime
# Create your views here.


def demo(request, id, pk):
    menu = MenuTable.objects.select_related('category').filter(res_id=id,  status='available')
    cat = Categories.objects.filter(rest_id=id)
    table = Table.objects.select_related('rest').get(table_no=pk, rest_id=id)
    if table.status != 'Occupied':
        table.status = 'Occupied'
        table.save()
    cart = OrderItem.objects.select_related('product').filter(
        table_no__table_no=pk, table_no__rest=id, ordered=False, product__status = 'available', status='pending')
    cartCount = 0
    for i in cart.values():
        cartCount = cartCount + i['quantity']
    return render(request, 'new_userpanel/index.html', {'menu': menu, 'table': table, 'cart': cart, 'cat': cat, 'cartCount':cartCount})


# def add_to_cart_ajax(request):
#     id = request.POST.get('id')
#     pk = request.POST.get('table')
#     item = get_object_or_404(MenuTable, id=id)
#     table = get_object_or_404(Table, id=pk, rest_id=item.res_id)

#     order, created = Order.objects.get_or_create(
#         table_no=table, ordered=False, status='Pending',
#         defaults={'ordered_date': timezone.now()}
#     )

#     order_item, created = OrderItem.objects.update_or_create(
#         product=item, table_no=table, ordered=False, status='pending',
#         defaults={'quantity': F('quantity') + 1}
#     )

#     if created or order.item.filter(product=item, status='pending').count() == 0:
#         print("------", order)
#         order.item.add(order_item)
#         messages.info(request, "Item was added to cart")
#         qty = 1
#     else:
#         print('<<<<', order_item.quantity)
#         qty = order_item.quantity
#     print('>>>>>>>>',qty)
#     return JsonResponse({'status': 'True'})

def add_to_cart_ajax(request):
    id = request.POST.get('id')
    pk = request.POST.get('table')
    item = get_object_or_404(MenuTable, id=id)
    table = get_object_or_404(Table, id=pk, rest_id=item.res_id)

    order, created = Order.objects.get_or_create(
        table_no=table, ordered=False, status='Pending',
        defaults={'ordered_date': timezone.now()}
    )

    order_item, created = OrderItem.objects.get_or_create(
        product=item, table_no=table, ordered=False, status='pending',
        defaults={'quantity': 1}  # Set initial quantity to 1
    )

    if not created:
        # Item exists, increment the quantity using F expression
        OrderItem.objects.filter(
            product=item, table_no=table, ordered=False, status='pending'
        ).update(quantity=F('quantity') + 1)
        order_item.refresh_from_db()

    order.item.add(order_item)
    messages.info(request, "Item was added to cart")
    qty = order_item.quantity

    return JsonResponse({'status': 'True', 'qty': qty})

def menu_list(request, id, pk):
    menu = MenuTable.objects.filter(res_id=id,  status='available')
    cat = Categories.objects.filter(rest_id=id)
    table = Table.objects.get(table_no=pk, rest_id=id)
    user = User.objects.get(id=id)
    table.status = 'Occupied'
    table.save()
    cart = OrderItem.objects.filter(
        table_no__table_no=pk, table_no__rest=id, ordered=False, status='pending')
    print(cart)
    return render(request, 'customer/menu.html', {'menu': menu, 'table': table, 'cart': cart, 'cat': cat, 'user': user})


def add_to_cart(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        product=item, table_no__rest=item.res_id, table_no_id=pk, ordered=False, status='pending')
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=True, status='Pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk, status='pending').exists() or order.item.filter(product_id=item.pk, status='Preparing'):
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item Quantity was Updated")
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
        else:
            messages.info(request, "item was added to cart")
            order.item.add(order_item)
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
    else:
        ordered_date = datetime.datetime.now()
        order = Order.objects.create(
            table_no_id=pk, ordered_date=ordered_date,  ordered=True, status='Pending')
        order.item.add(order_item)
        messages.info(request, "item was added to cart")
    return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)


def remove_from_cart(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=False, status='Pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                product=item, table_no_id=pk, ordered=False, status='pending', table_no__rest=item.res_id)[0]
            order.item.model.delete(order_item)
            messages.info(request, "Item was removed from cart")
            return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)
        else:
            messages.info(request, "Item was not in your cart")
            return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)
    else:
        messages.info(request, "You do not have active order")
        return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)


def remove_item_from_cart(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=False, status='Pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                product=item, table_no_id=pk, ordered=False, status='pending', table_no__rest=item.res_id)[0]
            order.item.model.delete(order_item)
            
            messages.info(request, "Item was removed from cart")
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
        else:
            messages.info(request, "Item was not in your cart")
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
    else:
        messages.info(request, "You do not have active order")
        return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)

def remove_single_item_from_cart(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=False, status='Pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                product=item, table_no_id=pk, ordered=False, status='pending', table_no__rest=item.res_id)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.model.delete(order_item)
            messages.info(request, "Item was removed from cart")
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
        else:
            messages.info(request, "Item was not in your cart")
            return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)
    else:
        messages.info(request, "You do not have active order")
        return redirect("restaurant:menu", id=table.rest.id, pk=table.table_no)


def order_summary(request, id, id2):
    try:
        cart = OrderItem.objects.filter(
            table_no__table_no=id2, table_no__rest=id, ordered=False, status='pending', product__status = 'available').annotate(
            total_item_cost=F('product__Price') * F('quantity')
            )

        # Cart Total 
        total_cost = cart.aggregate(total=Sum('total_item_cost'))['total'] or 0

        table = Table.objects.get(table_no=id2, rest_id=id)
        orders = Order.objects.get(
            table_no__table_no=id2, table_no__rest=id, ordered=False, status='Pending')
        return render(request, 'new_userpanel/cart.html', {'cart': cart, 'orders': orders, 'table': table})
    except:
        cart = OrderItem.objects.filter(
            table_no__table_no=id2, table_no__rest=id, ordered=False, product__status = 'available', status='pending')
        table = Table.objects.get(table_no=id2, rest_id=id)
        return render(request, 'new_userpanel/cart.html', {'cart': cart, 'table': table})


def comment(request, id):
    cart = OrderItem.objects.get(id=id)
    a = request.GET.get(f'com{id}')

    cart.comment = a
    cart.save()
    return redirect('restaurant:order_summary', id=cart.table_no.rest.id, id2=cart.table_no.table_no)


def proceed_to_pay(request, id, id2):
    cart = OrderItem.objects.filter(
        table_no__table_no=id2, table_no__rest=id, ordered=False)
    orders = Order.objects.get(
        table_no__table_no=id2, table_no__rest=id, ordered=False, status='Pending')

    orders.ordered = True
    orders.ordered_date = datetime.datetime.now()
    orders.status = 'Pending'
    orders.save()

    for i in cart:
        # i.status = 'complete'
        i.ordered = True
        i.save()

    messages.warning(request, "New order ")
    messages.error(request, "order placed succesfully")
    return redirect('restaurant:demo', id=orders.table_no.rest.id, pk=orders.table_no.table_no)


def index(request):
    return render(request, 'index.html', {})


def call_a_waiter(request, id):
    tab_no = Table.objects.get(id=id)
    messages.warning(request, f'Table No: {tab_no.table_no} Need A Waiter')
    waiter_call = CallWaiter(table=tab_no, Status=True)
    waiter_call.save()
    return HttpResponse("waiter is comming sir")


def add_to_cart_order(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        product=item, table_no__rest=item.res_id, table_no_id=pk, ordered=False, status='pending')
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=False, status='Pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk, status='pending').exists() or order.item.filter(product_id=item.pk, status='Preparing'):
            order_item.quantity += 1
            order_item.save()
            order.item.add(order_item)
            messages.info(request, "Item Quantity was Updated")
            return JsonResponse({"status": 1})
            # return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)
        else:
            messages.info(request, "item was added to cart")
            order.item.add(order_item)
            return JsonResponse({"status": 1})
            # return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            table_no_id=pk, ordered_date=ordered_date,  ordered=False, status='Pending')
        order.item.add(order_item)
        messages.info(request, "item was added to cart")
    return JsonResponse({"status": 1})
    # return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)


def remove_single_item_from_cart_order(request, id, pk):
    item = get_object_or_404(MenuTable, id=id)
    order_qs = Order.objects.filter(
        table_no_id=pk, ordered=False, status='Pending', table_no__rest=item.res_id)
    table = Table.objects.get(id=pk)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(product_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                product=item, table_no_id=pk, ordered=False, status='pending', table_no__rest=item.res_id)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.item.model.delete(order_item)
            messages.info(request, "Item was removed from cart")
            return JsonResponse({"status": 1})
            # return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)
        else:
            messages.info(request, "Item was not in your cart")
            return JsonResponse({"status": 1})
            # return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)
    else:
        messages.info(request, "You do not have active order")
        return JsonResponse({"status": 1})
        # return redirect("restaurant:order_summary", id=table.rest.id, id2=table.table_no)

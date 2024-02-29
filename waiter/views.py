from django.http import HttpResponse
from accounts.models import User
from rest_admin.models import *
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
import datetime

# Create your views here.
def index(request):
    return HttpResponse('Hello Waiter')


def table_view(request):
    restro = User.objects.get(id=request.user.rest_id)

    tables = Table.objects.filter(rest_id=request.user.rest_id)
    return render(request, 'waiter/tables.html', {
        'tables': tables,
        'restro': restro
    })


from django.forms import inlineformset_factory, Select, TextInput
from restaurant.models import *

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

        # form = IpdTreatmentForm(request.POST)
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
                        messages.info(request, "Item Quantity was Updated")
                        return redirect('waiter:table_view')
                        
                    else:
                        messages.info(request, "item was added to cart")
                        formset.save(commit=True)
                        order.item.add(i)
                        return redirect('waiter:table_view')
                        
                else:
                    ordered_date = timezone.now()
                    order = Order.objects.create(
                        table_no_id=id, ordered_date=ordered_date,  ordered=True, status='Pending')
                    formset.save(commit=True)
                    order.item.add(i)
                    
                    messages.info(request, "item was added to cart")
                    return redirect('waiter:table_view')
        
            return redirect('waiter:table_view')

        else:
            print(formset.errors)
            
    else:
        formset = order_formset()

    return render(request, 'waiter/manual_order.html', {'formset': formset, 'restro': restro, 'table': table})



def today_order(request):
    restro = User.objects.get(id=request.user.rest_id)
    res = User.objects.get(id=request.user.rest_id)
    order_list = Order.objects.filter(table_no__rest_id=res.id, ordered=True,
                                      ordered_date__day=datetime.datetime.today().day, status='Pending')
    print(order_list)
    return render(request, 'waiter/today_order.html', {'order_list': order_list, 'restro': restro})

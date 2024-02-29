from django.template.loader import get_template
from .utils import render_to_pdf  # created in step 4
from django.views.generic import View
from django.http import HttpResponse
import datetime
from datetime import date
from django.contrib import messages
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse
from .models import *
from .forms import *
from accounts.forms import RestaurantForm
from accounts.models import User
from restaurant.models import *
from django.db.models import Count
from itertools import chain

# Create your views here.
def t_price(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    order_list =  Order.objects.filter(table_no__rest=res.id, ordered=True, status="complete",
                    start_date__date__day=datetime.datetime.today().day,
                    start_date__date__month=datetime.datetime.today().month,
                    start_date__date__year=datetime.datetime.today().year)

    parcel_order_list = Parcel_Order.objects.filter(customer__rest=res.id, ordered=True, status="complete",
                    start_date__date__day=datetime.datetime.today().day,
                    start_date__date__month=datetime.datetime.today().month,
                    start_date__date__year=datetime.datetime.today().year)

    order_list2 = Order.objects.filter(table_no__rest=res.id, ordered=True, status="complete",
                    start_date__date__month=datetime.datetime.today().month,
                    start_date__date__year=datetime.datetime.today().year)

    parcel_order_list2 = Parcel_Order.objects.filter(customer__rest=res.id, ordered=True, status="complete",
                    start_date__date__month=datetime.datetime.today().month,
                    start_date__date__year=datetime.datetime.today().year)
    
    total_emp = User.objects.filter(rest_id=request.user, is_employee=True)

    total_earn = Order.objects.filter(
        table_no__rest_id=res.id, ordered=True)

    parcel_total_earn = Parcel_Order.objects.filter(
        customer__rest_id=res.id, ordered=True)

    total_1 = 0
    total_2 = 0

    m_total_1 = 0
    m_total_2 = 0

    a_total_1 = 0
    a_total_2 = 0

    total = 0
    m_total = 0
    a_total = 0

    for i in order_list:
        total_1 += i.gst_total()

    for a in parcel_order_list:
        total_2 += a.gst_total()

    total = total_1 + total_2


    for j in order_list2:
        m_total_1 += j.gst_total()

    for b in parcel_order_list2:
        m_total_2 += b.gst_total()

    m_total = m_total_1 + m_total_2


    for k in total_earn:
        a_total_1 += k.gst_total()

    for c in parcel_total_earn:
        a_total_2 += c.gst_total()

    a_total = a_total_1 + a_total_2


    ### month bar chart ######
    month = [1,2,3,4,5,6,7,8,9,10,11,12]

    months_earn = []
    
    calc = 0

    for i in month:
        data_1 = Order.objects.filter(table_no__rest=res.id, ordered=True, status="complete", start_date__date__month=i, start_date__date__year=2021)
        data_2 = Parcel_Order.objects.filter(customer__rest=res.id, ordered=True, status="complete", start_date__date__month=i, start_date__date__year=2021)
        
        data = list(chain(data_1, data_2))

        if not data:
            months_earn.append(0)
        else:
            for j in data:     
                calc += j.gst_total()
            
            months_earn.append(calc)
            calc = 0

    ########## best seller bar chart ########

    best_data = OrderItem.objects.filter(table_no__rest=res.id, ordered=True, date__date__month=datetime.datetime.today().month,date__date__year=datetime.datetime.today().year)
    # best_data = Parcel_OrderItem.objects.filter(customer__rest=res.id, ordered=True, date__date__month=datetime.datetime.today().month,date__date__year=datetime.datetime.today().year)
    
    # best_data = chain(best_data_1, best_data_2)

    
    dish_count = []

    dish_name = []

    top_sell = best_data.values_list('product_id').annotate(product_count=Count('product_id')).order_by('-product_count')[:10]
    
    for i in top_sell:
        dish_name.append(MenuTable.objects.get(id=i[0]).Dish_Name)
        dish_count.append(i[1])

    ########## expenses ############
    year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day_earn_1 = Order.objects.filter(table_no__rest_id=res.id, ordered=True, start_date__year=year,
                                        start_date__month=month)
    day_earn_2 = Parcel_Order.objects.filter(customer__rest_id=res.id, ordered=True, start_date__year=year,
                                        start_date__month=month)

    day_earn = list(chain(day_earn_1, day_earn_2))         

    day_total = 0
    
    for i in day_earn:
        day_total += i.gst_total()
                        
    day_expense = Expenses.objects.filter(res_id=res.id, Date__year=year, Date__month=month)

    expense_total = 0
    for i in day_expense:
        expense_total += i.Day_Expense + i.Others


    per_month_expense = PerMonthExpenses.objects.filter(res_id=res.id, Date__date__year=year, Date__date__month=month)

    month_expense = 0 

    for i in per_month_expense:

        month_expense = i.Rent + i.Light_Bill + i.Others


    salary = User.objects.filter(rest_id=res.id, is_employee=True)

    sal = 0

    for i in salary:
        sal += i.salary
    
    assests_total = Assests.objects.filter(res_id=res.id, Date__date__year=year, Date__date__month=month)
    
    a_total = 0

    for i in assests_total:
        a_total += i.Furnishing + i.Kitchen_equipements + i.Others
    

    final_earn = a_total + day_total

    final_Expense = sal + month_expense + expense_total
    

    return render(request, 'rest_admin/t_earn.html', {'total': total, 'm_total': m_total, 'total_emp': total_emp,
                                                      'a_total': a_total, 'restro': restro, 'months_earn':months_earn,'dish_name':dish_name,'dish_count':dish_count, 'final_earn':final_earn, 'final_Expense':final_Expense})


def qr(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = QrForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.rest = res
            form_r.status = 'available'
            form_r.save()
            return redirect('rest_admin:table_list')
        else:
            print(form.errors)
    else:
        form = QrForm()
    return render(request, 'rest_admin/index.html', {
        'form': form,
        'restro': restro
    })


def add_menu(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = AddMenuForm(res.id, request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.res = res
            form_r.status = 'available'
            form_r.save()
            return redirect('rest_admin:menu_list')
        else:
            print(form.errors)
    else:
        form = AddMenuForm(res.id)
    return render(request, 'rest_admin/add_menu.html', {
        'form': form,
        'restro': restro
    })


def add_employee(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.set_password(form_r.password)
            form_r.rest = res
            form_r.is_employee = True
            form_r.save()
            return redirect('rest_admin:emp_list')
        else:
            print(form.errors)
    else:
        form = EmployeeForm()

    return render(request, 'rest_admin/add_employee.html', {
        'form': form,
        'restro': restro
    })


def add_categories(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = AddCategoryForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.rest = res
            form_r.save()
            return redirect('rest_admin:cat_list')
        else:
            print(form.errors)
    else:
        form = AddCategoryForm()
    return render(request, 'rest_admin/add_category.html', {
        'form': form,
        'restro': restro
    })


def category_list(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    cat_list = Categories.objects.filter(rest_id=res)
    return render(request, 'rest_admin/cat_list.html', {
        'cat_list': cat_list,
        'restro': restro
    })


def menu_list(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    menu_lists = MenuTable.objects.filter(res_id=res)
    return render(request, 'rest_admin/menu_list.html', {
        'menu_lists': menu_lists,
        'restro': restro
    })


def employee_list(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    emp_lists = User.objects.filter(is_employee=True, rest_id=res.id)
    print(emp_lists)
    return render(request, 'rest_admin/emp_list.html', {
        'emp_lists': emp_lists,
        'restro': restro
    })


def cat_form_edit(request, id):
    restro = User.objects.get(id=request.user.id)
    instance = get_object_or_404(Categories, id=id)

    form = AddCategoryForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:cat_list')
    return render(request, 'rest_admin/cat_edit.html', {
        'form': form,
        'restro': restro
    })


def delete(request, id):
    user2 = Categories.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('rest_admin:cat_list'))


def emp_form_edit(request, id):
    restro = User.objects.get(id=request.user.id)
    instance = get_object_or_404(User, id=id)
    form = EmployeeForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()

        return redirect('rest_admin:emp_list')
    else:
        print(form.errors)
    return render(request, 'rest_admin/emp_edite.html', {
        'form': form,
        'restro': restro
    })


def emp_delete(request, id):
    user2 = User.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('rest_admin:emp_list'))


def menu_form_edit(request, id):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    instance = get_object_or_404(MenuTable, id=id)

    form = AddMenuForm(res, request.POST or None, request.FILES or None, instance=instance)
    print('>>>>', restro,request.FILES)
    if form.is_valid():
        form.save()
        return redirect('rest_admin:menu_list')
    return render(request, 'rest_admin/edit_menu.html', {
        'form': form,
        'restro': restro
    })


def menu_delete(request, id):
    user2 = MenuTable.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('rest_admin:menu_list'))


def menu_avc(request, id):
    item = MenuTable.objects.get(id=id)
    if item.status == 'available':
        item.status = 'Not Available'
        item.save()
    else:
        item.status = 'available'
        item.save()

    return HttpResponseRedirect(reverse('rest_admin:menu_list'))


def table_view(request):
    restro = User.objects.get(id=request.user.id)

    tables = Table.objects.filter(rest_id=request.user)
    return render(request, 'rest_admin/tables.html', {
        'tables': tables,
        'restro': restro
    })


def table_list(request):
    restro = User.objects.get(id=request.user.id)

    tables = Table.objects.filter(rest_id=request.user)
    return render(request, 'rest_admin/table_list.html', {
        'tables': tables,
        'restro': restro
    })


def table_edit(request, id):
    instance = Table.objects.get(id=id)

    form = QrForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        return redirect('rest_admin:table_list')
    else:
        print(form.errors)
    return render(request, 'rest_admin/table_u.html', {'form': form})


def table_delete(request, id):
    user2 = Table.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('rest_admin:table_list'))




def report(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    month = request.GET.get('month')
    year = request.GET.get('year')
    result = OrderItem.objects.filter(table_no__rest_id=res.id, ordered=True, date__year=year,
                                        date__month=month)

    m_total = 0
    for i in result:
        m_total += i.product.Price
    messages.success(request, f'Months Income:{m_total} ')
    return render(request, 'rest_admin/report.html', {'m_total': m_total, 'restro': restro})


def orders(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        if request.POST.get('fromDate') and request.POST.get('toDate'):
            from_date = request.POST.get('fromDate')
            to_date = request.POST.get('toDate')
            order_list = Order.objects.filter(
                ordered_date__range=[from_date, to_date])
        else:
            messages.error(request, 'Enter valid date')
            return redirect('rest_admin:orders')
    else:
        order_list = Order.objects.filter(
            table_no__rest_id=res.id, ordered=True)

    return render(request, 'rest_admin/orders.html', {'order_list': order_list, 'restro': restro})


def order_details(request, id):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    order_det = Order.objects.get(id=id)
    return render(request, 'rest_admin/order_details.html', {'order_det': order_det, 'user': res, 'restro': restro})


def today_order(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    today = date.today()
    order_list = Order.objects.filter(table_no__rest_id=res.id, ordered=True,
                 ordered_date__contains=today, status='Pending')
    parcel_order_list = Parcel_Order.objects.filter(customer__rest_id=res.id, ordered=True,
                 ordered_date__contains=today, status='Pending')
   
    return render(request, 'rest_admin/today_order.html', {'parcel_order_list': parcel_order_list, 'order_list': order_list, 'restro': restro})


def order_complete(request, id):

    o_state = Order.objects.get(id=id)
    o_state.status = 'Complete'
    o_state.save()
    table = Table.objects.get(table_no=o_state.table_no.table_no)
    table.status = 'available'
    table.save()
    return render(request, 'rest_admin/payment.html', {'o_state': o_state})


class GeneratePdf(View):
    def get(self, request, id):
        o_state = Order.objects.get(id=id)
        o_state.status = 'Complete'
        o_state.save()
        table = Table.objects.get(table_no=o_state.table_no.table_no, rest= request.user)
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
        pdf = render_to_pdf('rest_admin/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


def user_details(request):
    restro = User.objects.get(id=request.user.id)
    user = User.objects.get(id=request.user.id)
    return render(request, 'rest_admin/user_profile.html', {'user': user, 'restro': restro})


def update_details(request, id):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    instance = get_object_or_404(User, id=res.id)

    form = RestaurantForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:user_profile')
    else:
        print(form.errors)
    return render(request, 'rest_admin/update_u.html', {'form': form, 'restro': restro})


def com_edit(request, id):
    instance = get_object_or_404(OrderItem, id=id)

    form = ComForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()

        return redirect('rest_admin:t_order')
    else:
        print(form.errors)
    return render(request, 'rest_admin/com_u.html', {'form': form})


def add_manager(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.set_password(form_r.password)
            form_r.rest = res
            form_r.is_employee = True
            form_r.is_manager = True
            form_r.save()
            return redirect('rest_admin:manager_list')
        else:
            print(form.errors)
    else:
        form = EmployeeForm()

    return render(request, 'rest_admin/add_manager.html', {
        'form': form,
        'restro': restro
    })


def manager_list(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    emp_lists = User.objects.filter(
        is_employee=True, is_manager=True, rest_id=res.id)

    return render(request, 'rest_admin/manager_list.html', {
        'emp_lists': emp_lists,
        'restro': restro
    })


def manager_form_edit(request, id):
    restro = User.objects.get(id=request.user.id)
    instance = get_object_or_404(User, id=id)
    form = EditEmployeeForm(
        request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        form.save()

        return redirect('rest_admin:manager_list')
    else:
        print(form.errors)
    return render(request, 'rest_admin/manager_edite.html', {
        'form': form,
        'restro': restro
    })


def manager_delete(request, id):
    user2 = User.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('rest_admin:manager_list'))


def add_day_expenses(request):
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = ExpensesForm(request.POST, request.FILES)
        
        if form.is_valid():
            form_r = form.save(commit=False)
            form_r.res = res
            form_r.save()
            return redirect('rest_admin:manage_day_expenses')
        else:
            print(form.errors)
    else:
        form = ExpensesForm()
    return render(request, 'rest_admin/add_day_expenses.html', {'form': form})


def manage_day_expenses(request):
    data = Expenses.objects.filter(res_id=request.user.id)
    return render(request, 'rest_admin/manage_day_expenses.html', {'data': data})


def edit_expenses(request, id):

    restro = User.objects.get(id=request.user.id)
    instance = get_object_or_404(Expenses, id=id)

    form = EditExpensesForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:manage_day_expenses')

    else:
        print(form.errors)

    return render(request, 'rest_admin/edit_day_expenses.html', {'form': form, 'restro': restro})


def add_month_expenses(request):
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = PerMonthExpensesForm(request.POST, request.FILES)

        my_list = []
        
        month = PerMonthExpenses.objects.all()
        for i in month:
            m = i.Date.month
            y = i.Date.year
            my = f'{m},{y}'
            my_list.append(my)


        if form.is_valid():
            form_r = form.save(commit=False)
            print("formmm", form_r.Date.month)

            for date in my_list:
                if f'{form_r.Date.month},{form_r.Date.year}' == date:
                    messages.success(request, f"You already Entered {form_r.Date.month},{form_r.Date.year}'s Expenses.")
                    return redirect('rest_admin:add_month_expenses')

            else:
                form_r.res = res
                form_r.save()
                return redirect('rest_admin:manage_month_expenses')
        else:
            print(form.errors)
    else:
        form = PerMonthExpensesForm()
    return render(request, 'rest_admin/add_month_expenses.html', {'form': form})

 
def manage_month_expenses(request):
    data = PerMonthExpenses.objects.filter(res_id=request.user.id)

    return render(request, 'rest_admin/manage_month_expenses.html', {'data': data})



def edit_expenses(request, id):
    restro = User.objects.get(id=request.user.id)
    data = Expenses.objects.get(id=id)
    
    form = EditExpensesForm(request.POST or None, instance=data)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:user_profile')
    else:
        print(form.errors)
    return render(request, 'rest_admin/update_u.html', {'form': form, 'restro': restro})


def edit_month_expenses(request, id):
    restro = User.objects.get(id=request.user.id)
    instance = get_object_or_404(PerMonthExpenses, id=id)

    form = EditMonthExpensesForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:manage_month_expenses')

    else:
        print(form.errors)

    return render(request, 'rest_admin/edit_month_expenses.html', {'form': form, 'restro': restro})


def balence_sheet(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    try:
        if request.GET.get('month') != None and request.GET.get('year') != None:
            month = request.GET.get('month')
            year = request.GET.get('year')
        else:
            raise EOFError()

        day_earn = OrderItem.objects.filter(table_no__rest_id=res.id, ordered=False, date__year=year,
                                        date__month=month)

        day_total = 0
        
        for i in day_earn:
            day_total += i.get_total_item_price()
                                       
        day_expense = Expenses.objects.filter(res_id=res.id, Date__year=year, Date__month=month)

        expense_total = 0
        for i in day_expense:
            expense_total += i.Day_Expense + i.Others

        per_month_expense = PerMonthExpenses.objects.filter(res_id=res.id, Date__date__year=year, Date__date__month=month)
        
        month_expense = 0 

        for i in per_month_expense:

            month_expense = i.Rent + i.Light_Bill + i.Others

        
        salary = User.objects.filter(rest_id=res.id, is_employee=True)

        sal = 0

        for i in salary:
            sal += i.salary
        
        assests_total = Assests.objects.filter(res_id=res.id, Date__date__year=year, Date__date__month=month)
        
        a_total = 0

        for i in assests_total:
            a_total += i.Furnishing + i.Kitchen_equipements + i.Others
        
        final_earn = a_total + day_total

        final_Expense = sal + month_expense + expense_total 
    
        return render(request, 'rest_admin/report.html', {'restro': restro, 'day_total':day_total, 'per_month_expense':per_month_expense, 'expense_total':expense_total, 'sal':sal, 'final_Expense':final_Expense, 'final_earn': final_earn, 'assests_total':assests_total, 'month':month, 'year': year})
    except:
        month = date__year=datetime.datetime.today().month
        year = date__year=datetime.datetime.today().year
        day_earn = OrderItem.objects.filter(table_no__rest_id=res.id, ordered=True, date__year=year,
                                        date__month=month)

        day_total = 0
        
        for i in day_earn:
            day_total += i.get_total_item_price()
                            
        day_expense = Expenses.objects.filter(res_id=res.id, Date__year=year, Date__month=month)

        expense_total = 0
        for i in day_expense:
            expense_total += i.Day_Expense + i.Others
    

        per_month_expense = PerMonthExpenses.objects.filter(res_id=res.id, Date__date__year=year, Date__date__month=month)

        month_expense = 0 

        for i in per_month_expense:

            month_expense = i.Rent + i.Light_Bill + i.Others


        salary = User.objects.filter(rest_id=res.id, is_employee=True)

        sal = 0

        for i in salary:
            sal += i.salary
        
        assests_total = Assests.objects.filter(res_id=res.id, Date__date__year=year, Date__date__month=month)
        
        a_total = 0

        for i in assests_total:
            a_total += i.Furnishing + i.Kitchen_equipements + i.Others
        

        final_earn = a_total + day_total

        final_Expense = sal + month_expense + expense_total
    
        return render(request, 'rest_admin/report.html', { 'restro': restro, 'day_total':day_total, 'per_month_expense':per_month_expense, 'expense_total':expense_total, 'sal':sal, 'final_Expense':final_Expense, 'final_earn':final_earn, 'assests_total':assests_total, 'month':month, 'year': year})


def add_assests(request):
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = AssestsForm(request.POST, request.FILES)

        if form.is_valid():
            form_r = form.save(commit=False)
            form_r.res = res
            form_r.save()
            return redirect('rest_admin:manage_assests')
        else:
            print(form.errors)
    else:
        form = AssestsForm()
    return render(request, 'rest_admin/add_assests.html', {'form': form})

 
def manage_assests(request):
    data = Assests.objects.filter(res_id=request.user.id)

    return render(request, 'rest_admin/manage_assets.html', {'data': data})



def edit_assests(request, id):
    restro = User.objects.get(id=request.user.id)
    data = Assests.objects.get(id=id)
    form = AssestsForm(request.POST or None, instance=data)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:manage_assests')
    else:
        print(form.errors)
    return render(request, 'rest_admin/update_assests.html', {'form': form, 'restro': restro})


def add_unit(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = AddUnitForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.rest = res
            form_r.save()
            return redirect('rest_admin:unit_list')
        else:
            print(form.errors)
    else:
        form = AddUnitForm()
    return render(request, 'rest_admin/add_unit.html', {
        'form': form,
        'restro': restro
    })


def unit_list(request):
    data = Unit.objects.filter(rest_id=request.user.id)
 
    return render(request, 'rest_admin/unit_list.html', {'data': data})

def edit_unit(request, id):
    restro = User.objects.get(id=request.user.id)
    instance = get_object_or_404(Unit, id=id)

    form = AddUnitForm(request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:unit_list')

    else:
        print(form.errors)

    return render(request, 'rest_admin/edit_unit.html', {'form': form, 'restro': restro})


def delete_unit(request, id):
    data = Unit.objects.get(id=id)
    data.delete()

    return redirect('rest_admin:unit_list')


def add_inventory(request):
    restro = User.objects.get(id=request.user.id)
    res = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = AddInventoryForm(res, request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.rest = res
            form_r.save()
            return redirect('rest_admin:inventory_list')
        else:
            print(form.errors)
    else:
        form = AddInventoryForm(res)
    return render(request, 'rest_admin/add_inventory.html', {
        'form': form,
        'restro': restro
    })


def inventory_list(request):
    data = Inventory.objects.filter(rest_id=request.user.id)
    
    return render(request, 'rest_admin/inventory_list.html', {'data': data})


def edit_inventory(request, id):
    restro = User.objects.get(id=request.user.id)
    instance = get_object_or_404(Inventory, id=id)

    form = AddInventoryForm(restro, request.POST or None, instance=instance)

    if form.is_valid():
        form.save()
        return redirect('rest_admin:inventory_list')

    else:
        print(form.errors)

    return render(request, 'rest_admin/update_inventory.html', {'form': form, 'restro': restro})

def delete_inventory(request, id):
    data = Inventory.objects.get(id=id)
    data.delete()

    return redirect('rest_admin:inventory_list')
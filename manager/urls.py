from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'manager'

urlpatterns = [
    path('qr/', views.qr, name='qr'),
    path('add_menu/', views.add_menu, name='add_menu'),
    path('add_category/', views.add_categories, name='add_category'),
    path('cat_list/', views.category_list, name='cat_list'),
    path('menu_list/', views.menu_list, name='menu_list'),
    path('menu_state/<int:id>/', views.menu_avc, name='menu_state'),
    path('edit_cat/<int:id>/', views.cat_form_edit, name='edit_cat'),
    path('delete_cat/<int:id>/', views.delete, name='delete_cat'),
    path('edit_menu/<int:id>/', views.menu_form_edit, name='edit_menu'),
    path('delete_menu/<int:id>/', views.menu_delete, name='delete_menu'),
    path('orders/', views.orders, name='orders'),
    path('t_orders/', views.today_order, name='t_order'),
    path('orders_det/<int:id>/', views.order_details, name='order_det'),
    path('complete/<int:id>/', views.order_complete, name='order_complete'),
    path('pdf/<int:id>/', views.GeneratePdf.as_view(), name='pdf'),
    path('menu_state/<int:id>/', views.menu_avc, name='menu_state'),
    path('user_profile/', views.user_details, name='user_profile'),
    path('update_u/<int:id>/', views.update_details, name='update_u'),

    path('', views.table_view, name='table_view'),
    path('edit_table/<int:id>/', views.table_edit, name='edit_table'),
    path('delete_table/<int:id>/', views.table_delete, name='delete_table'),

    path('table_list/', views.table_list, name='table_list'),
    path('com_u/<int:id>/', views.com_edit, name='com_u'),
    path('manual_order/<int:id>/', views.manual_order, name='manual_order'),
    path('add_customer', views.add_customer, name='add_customer'),
    path('manual_order_parcel/', views.manual_order_parcel, name='manual_order_parcel'),
    path('parcel_pdf/<int:id>/', views.Parcel_GeneratePdf.as_view(), name='parcel_pdf'),
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
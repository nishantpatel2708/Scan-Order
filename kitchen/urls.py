from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'kitchen'

urlpatterns = [

    path('', views.table_view, name='table_view'),
    path('cat_list/', views.category_list, name='cat_list'),
    path('menu_list', views.menu_list, name='menu_list'),
    path('orders/', views.orders, name='orders'),
    path('t_orders/', views.today_order, name='t_order'),
    path('orders_det/<int:id>/', views.order_details, name='order_det'),
    path('P_state/<int:id>/', views.status_preparing, name='p_state'),
    path('rts_state/<int:id>/', views.status_ready_to_serve, name='rts_state'),
    path('add_menu/', views.add_menu, name='add_menu'),
    path('add_category/', views.add_categories, name='add_category'),
    path('user_d/', views.user_info, name='user_d'),
    path('menu_state/<int:id>/', views.menu_state, name='menu_state'),
    path('parcel_P_state/<int:id>/', views.parcel_status_preparing, name='parcel_p_state'),
    path('parcel_rts_state/<int:id>/', views.parcel_status_ready_to_serve, name='parcel_rts_state'),
    


] + static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
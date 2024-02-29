from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.index, name='index'),
    path('menu_demo/<int:id>/<int:pk>/', views.demo, name='demo'),
    path('menu/<int:id>/<int:pk>/', views.menu_list, name='menu'),
    path('add_to_cart_ajax/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('add_to_cart/<int:id>/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_s_from_cart/<int:id>/<int:pk>/', views.remove_single_item_from_cart, name='remove_single'),
    path('order_summary/<int:id>/<int:id2>/', views.order_summary, name='order_summary'),
    path('place_order/<int:id>/<int:id2>/', views.proceed_to_pay, name='place_order'),
    path('call_waiter/<int:id>/', views.call_a_waiter, name='call_waiter'),
    path('com/<int:id>/', views.comment, name='com'),
    path('add_to_cart_order/<int:id>/<int:pk>/', views.add_to_cart_order, name='add_to_cart_order'),
    path('remove_from_cart_order/<int:id>/<int:pk>/', views.remove_single_item_from_cart_order, name='remove_from_cart_order'),
    path('demo/<int:id>/<int:pk>/', views.demo, )

] + static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

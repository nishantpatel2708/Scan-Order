from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'waiter'

urlpatterns = [
    path('', views.table_view, name='table_view'),
    path('manual_order/<int:id>/', views.manual_order, name='manual_order'),
    path('t_orders/', views.today_order, name='t_order'),
] + static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

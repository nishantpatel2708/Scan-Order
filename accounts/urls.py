from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.r_register, name="register"),
    path('', views.user_login, name='login'),
    path('user_logout/', views.user_logout, name='user_logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

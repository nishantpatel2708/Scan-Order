from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, redirect
from .forms import *
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


def r_register(request):

    if request.method == 'POST':

        form = RestaurantForm(request.POST, request.FILES)

        if form.is_valid():

            form_r = form.save(commit=False)
            form_r.set_password(form_r.password)

            form_r.is_rest = True

            if 'profile_photo' in request.FILES:
                form_r.profile_photo = request.FILES['profile_photo']

            form_r.save()
            return HttpResponseRedirect(reverse('accounts:index'))

        else:
            print(form.errors)
            return Http404("Some Errors Occur")
    else:
        form = RestaurantForm()
    return render(request, 'register/register_page.html', {'form': form})


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active and user.is_rest:

                login(request, user)

                return HttpResponseRedirect(reverse('rest_admin:t_price'))
            elif user.is_active and user.is_employee and user.is_manager:

                login(request, user)

                return HttpResponseRedirect(reverse('manager:table_view'))
            elif user.is_active and user.is_employee and user.Category == 'chef':

                login(request, user)

                return HttpResponseRedirect(reverse('kitchen:table_view'))
            elif user.is_active and user.is_employee and user.Category == 'waiter':

                login(request, user)

                return HttpResponseRedirect(reverse('waiter:table_view'))

            else:

                messages.error(request, "Invalid login details supplied.")
                return redirect('accounts:login')
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            messages.error(request, "Invalid login details supplied.")
            return redirect('accounts:login')

    else:
        # Nothing has been provided for username or password.

        return render(request, 'register/login.html', {})


def user_logout(request):
    logout(request)
    return redirect('accounts:login')

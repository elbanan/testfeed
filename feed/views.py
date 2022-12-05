from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import *

# Create your views here.


# Login/Register Controllers
def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper_func


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return redirect('home')
		return wrapper_func
	return decorator


@unauthenticated_user
def register_view(request): 
    form = CreateUserForm()
    if request.method == 'POST':
        print (request.POST)
        form = CreateUserForm(request.POST)
        agree_tos = request.POST.get('tos')
        if agree_tos:
            if form.is_valid():
                new_user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'User '+request.POST.get('username')+' was created successfully. Please login below to proceed.')
                return (redirect('login'))
            else:
                messages.error(request, ' '.join([' '.join(x for x in l) for l in list(form.errors.values())]))
        else:
            messages.error(request, 'Please agree to Terms of Service.')
    page_content = {
                'registerform':form,
                }
    return render(request, "feed/register.html", {'page_content':page_content})


@unauthenticated_user #(CHECKED)
def login_view(request, *args, **kwargs): #(CHECKED)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect ('home')
        else:
            return render(request, "feed/login.html")
    else:
        return render(request, "feed/login.html")


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('/login')

@login_required(login_url='login')
def home_view(request):
        return render(request, "feed/base.html")
       


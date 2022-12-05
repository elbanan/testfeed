from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('access_denied/', views.logout_view, name='access_denied'),
    path('home/', views.home_view, name='home'),
    path('home', views.home_view, name='home'),
]

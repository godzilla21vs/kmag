from django.shortcuts import render
from .views import  RegisterView
from django.urls import path 
from django.contrib.auth.views import LoginView, LogoutView

# création des vues

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

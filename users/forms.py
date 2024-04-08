# from django.urls import path
# from .views import RegisterView
# from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html') name='logout')
#  ]

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
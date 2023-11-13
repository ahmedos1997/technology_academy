from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from .forms import UserLogin
from .views import RegisterView
# from . import forms



urlpatterns = [
    path('login/', LoginView.as_view(authentication_form=UserLogin), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('profile', views.editprofile, name='profile'),
    path('', include('django.contrib.auth.urls')),
]
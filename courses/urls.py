from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [

    path('', views.CourseListView, name='main'),
    path('my_path', views.My_path, name='my_path'),
    path('path_view/<int:id>', views.PathView, name='path_view'),
    path('replie_view/<int:id>', views.ReplieCreateView, name='replie_view'),
    path('subscribe/<int:id>', views.SubscriberCreateView, name='subscribe'),
    path('success', views.success, name='success')
    ]

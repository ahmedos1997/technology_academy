from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [

    path('blog_list', views.Blog_list, name='blog_list'),
    path('blog_create', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog_update/<int:pk>', views.BlogUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('blog_view/<int:id>', views.Blog_view, name='blog_view'),
]

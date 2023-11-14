from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [

    path('', views.CourseListView, name='main'),
    path('course_view<int:id>/', views.Course_view, name='course_view'),
    path('my_path/', views.My_path, name='my_path'),
    path('path_view<int:id/>', views.PathView, name='path_view'),
    path('replie_view<int:id/>', views.ReplieCreateView, name='replie_view'),
    path('checkout<int:id/>', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('change-language/', views.change_language, name='change_language'),
    path('create-checkout-session/<pk>', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [

    path('', views.CourseListView, name='main'),
    path('my_path', views.My_path, name='my_path'),
    path('path_view/<int:id>', views.PathView, name='path_view'),
    path('replie_view/<int:id>', views.ReplieCreateView, name='replie_view'),
    path('subscribe/<int:id>', views.Subscribe, name='subscribe'),
    path('success', views.success, name='success'),
    path('change-language/', views.change_language, name='change_language'),



    path('checkout/stripe/config/', views.stripe_config, name='checkout.stripe_config'),
    # path('stripe/webhook', webhook.stripe_webhook),
    path('checkout/stripe', views.stripe_transaction, name='checkout.stripe'),
    path('checkout/paypal', views.paypal_transaction, name='checkout.paypal'),
    # path('paypal/webhook', ipn, name='checkout.paypal-webhook'),
]
import math

from django.contrib.sessions.models import Session
from django.core.checks import translation
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import activate, gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from paypal.standard.forms import PayPalPaymentsForm

from. import models
from .models import Course, Path, Comment, Replie, Subscriber, Transaction, PaymentMethod
from . import forms
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import CommentCreateForm, ReplieCreateForm, SubscriberForm, UserInfoForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views import View
import stripe

from technology_academy import settings


# Create your views here.


# course code

def CourseListView(request):
    courses = Course.objects.all()
    user = request.user
    subscriber = []
    if user.is_authenticated:
        subscriber = Subscriber.objects.filter(user=user).values_list('course', flat=True)
    context = {
        'courses': courses,
        'subscriber': subscriber,
    }
    return render(request, 'page/main.html', context)




def My_path(request):
    user = request.user
    subscriber_paths = []
    paths=[]
    courses = []
    if user.is_authenticated:
        subscriber_paths = Subscriber.objects.filter(user=user).values_list('course__path', flat=True)
        paths = Path.objects.filter(pk__in=subscriber_paths)
        courses = Course.objects.filter(pk__in=paths)
    context = {
        'subscriber_paths': subscriber_paths,
        'paths':paths,
        'courses':courses
    }
    return render(request, 'page/my_path.html', context)


class CommentcreateView(CreateView):
    model = models.Course
    form_class = forms.CommentCreateForm
    template_name = 'page/path_view.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)




def PathView(request, id):
    path = Path.objects.get(id=id)
    form = CommentCreateForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.path = path
            comment.save()
        form.save()

    context = {
        'path':path,
        'form': form,
    }
    return render(request, 'page/path_view.html', context)




def ReplieCreateView(request, id):
    comment = Comment.objects.get(id=id)
    form = ReplieCreateForm(request.POST)
    user = request.user
    if request.method == 'POST':
        if form.is_valid():
            replie = form.save(commit=False)
            replie.comment = comment
            replie.user = user
            replie.save()
        form.save()
    context = {
        'form': form,
        'comment':comment
    }
    return render(request, 'page/replie_view.html', context)

################### stripe and payment and mail#############################






def success(request):
    return render(request, 'page/success.html')

def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            activate(language)
            request.session['django_language'] = language
    return HttpResponseRedirect(reverse('main'))


def send_order_mail(request, course):
    user = request.user
    msg_html = render_to_string('page/email.html',{
        'course':course,
        'user':user
    })
    recipient_list = request.user.email
    send_mail(
        subject='new order',
        html_message=msg_html,
        message=msg_html,
        from_email= 'example@example.com',
        recipient_list= [recipient_list]
    )

def Subscribe(request, id):
    user = request.user
    course = Course.objects.get(id=id)
    if request.method == 'POST':
        send_order_mail(request, course)
        return redirect('success')
    return render(request, 'page/checkout.html', {'course':course,'user':user})
######################### stripe ######################################

def stripe_config(request):
    return JsonResponse({
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })


def stripe_transaction(request):
    transaction = make_transaction(request, PaymentMethod.stripe)
    if not transaction:
        return JsonResponse({
            'message': _('please enter valid information.')
        }, status=400)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=transaction.amount * 100,
        currency=settings.CURRENCY,
        payment_method_types=['card'],
        metadata={
            'transaction': transaction.id
        }
    )
    return JsonResponse({
        'client_secret': intent['client_secret']
    })



def paypal_transaction(request):
    transaction = make_transaction(request, PaymentMethod.paypal)
    if not transaction:
        return JsonResponse({
            'message': _('please enter valid information.')
        }, status=400)

    form = PayPalPaymentsForm(initial={
        'business': settings.PAYPAL_EMAIL,
        'amount': transaction.amount,
        'invoice': transaction.id,
        'currency_code': settings.CURRENCY,
        'return_url': f'http://{request.get_host()}{reverse("store.checkout_complete")}',
        'cancel_url': f'http://{request.get_host()}{reverse("store.checkout")}',
        'notify_url': f'http://{request.get_host()}{reverse("checkout.paypal-webhook")}',


    })
    return HttpResponse(form.render())



def make_transaction(request, pm):

    form = UserInfoForm(request.POST)
    if form.is_valid():
        course = Course.objects.filter(id=id)


        return Transaction.objects.create(
            customer=form.cleaned_data,
            session=request.session.session_key,
            payment_method=pm,
            items=course.title,
            amount=math.ceil(course.price))


def send_order_email(order, products):
    msg_html = render_to_string('emails/order.html', {
        'order': order,
        'products': products

    })
    send_mail(
        subject='New order',
        html_message=msg_html,
        message=msg_html,
        from_email='ahmed@example.com',
        recipient_list=[order.customer['email']]


    )

# def SubscriberCreateView(request, id):
#     course = Course.objects.get(id=id)
#     user = request.user
#     form = forms.SubscriberForm(request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             subsc = form.save(commit=False)
#             subsc.course = course
#             subsc.email = user.email
#             subsc.price = course.price
#             subsc.user = user
#             subsc.save()
#         form.save()
#         return redirect('success')
#     context = {
#         'course': course,
#         'user': user,
#         'form': form
#     }
#     return render(request, 'page/checkout.html', context)
import math
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import activate, gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from. import models
from .models import Course, Path, Comment, Replie, Subscriber
from . import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import CommentCreateForm, ReplieCreateForm

from django.views import View
import stripe
from technology_academy import settings


# Create your views here.


# course code




def Course_view(request, id):
    course = Course.objects.get(id=id)
    user = request.user
    subscriber = []
    if user.is_authenticated:
        subscriber = Subscriber.objects.filter(user=user).values_list('course', flat=True)
    context = {
        'course': course,
        'subscriber': subscriber,
    }
    return render(request, 'page/course_view.html', context)
# def Course_view(request, id):
#     course = Course.objects.get(id=id)
#     user = request.user
#     subscriber = []
#     if user.is_authenticated:
#         subscriber = Subscriber.objects.filter(user=user).values_list('course', flat=True)
#     context = {
#         'course': course,
#         'subscriber': subscriber,
#     }
#     return render(request, 'page/course_view.html', context)
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
    user = request.user
    return render(request, 'page/success.html', {'user':user})

def cancel(request):
    return render(request, 'page/cancel.html')

def change_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            request.session['django_language'] = language
            activate(language)
    else:
        language = request.session.get('django_language')
        if language:
            activate(language)
    return HttpResponseRedirect(reverse('my_path'))


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


def checkout(request, id):
    course = Course.objects.get(id=id)
    user = request.user
    return render(request, 'page/checkout.html', {'course':course,'user':user})



# ######################### stripe ######################################
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        course = Course.objects.get(id=self.kwargs["pk"])
        # إنشاء المنتج (Product)
        product = stripe.Product.create(
            name=course.title,  # اسم المنتج
            type='service',  # نوع المنتج
            # images=course.image.url
        )

        # إنشاء كائن السعر (Price object) وربطه بالمنتج
        price = stripe.Price.create(
            unit_amount=course.price *100 ,  # قيمة السعر بالقرش المؤسسة (cents)
            currency='usd',  # العملة المستخدمة
            product=product.id,  # معرّف المنتج
        )



        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.id,  # استخدام معرف كائن السعر
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.BASE_URL + '/success',
            cancel_url=settings.BASE_URL + '/cancel',
        )
        send_order_mail(request, course)

        user = request.user
        subscriber = Subscriber()
        subscriber.name = user.username
        subscriber.course = course
        subscriber.email = user.email
        subscriber.price = course.price
        subscriber.user = request.user
        subscriber.save()
        return redirect(checkout_session.url)


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

#
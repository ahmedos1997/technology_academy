from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.sessions.models import Session
from stripe.api_resources.payment_intent import PaymentIntent


# Create your models here.
############# course ######################
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField()
    def __str__(self):
        return self.title



class Path(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video = models.FileField()
    def __str__(self):
        return self.title

    def get_comments(self):
        return Comment.objects.filter(path=self)



class Comment(models.Model):
    title = models.TextField()
    path = models.ForeignKey(Path, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.title

    def get_replies(self):
        return Replie.objects.filter(comment=self)




class Replie(models.Model):
    title = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.title



####################payment and checkout####################


class Subscriber(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    email = models.EmailField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name



class TransactionStatus(models.IntegerChoices):
    pending = 0, ('pending'),
    completed = 1, ('completed')



class PaymentMethod(models.IntegerChoices):
    stripe = 1, ('strip'),
    paypal = 2, ('paypal')


class Transaction(models.Model):
    session = models.CharField(max_length=255)
    amount = models.FloatField()
    items = models.JSONField()
    customer = models.JSONField()
    status = models.IntegerField(
        choices=TransactionStatus.choices, default=TransactionStatus.pending
    )

    payment_method = models.IntegerField(
        choices=PaymentMethod.choices
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def customer_name(self):
        return self.customer['first_name'] + ' ' + self.customer['last_name']

    @property
    def customer_email(self):
        return self.customer['email']

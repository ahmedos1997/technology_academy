# Generated by Django 4.2 on 2023-10-26 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_payment_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='transaction',
        ),
    ]

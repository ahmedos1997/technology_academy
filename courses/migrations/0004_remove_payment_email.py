# Generated by Django 4.2 on 2023-10-26 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_payment_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='email',
        ),
    ]

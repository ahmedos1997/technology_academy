# Generated by Django 4.2 on 2023-10-27 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_payment_remove_transaction_course_delete_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]

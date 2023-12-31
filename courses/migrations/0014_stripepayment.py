# Generated by Django 4.2 on 2023-10-30 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_rename_created_at_payment_create_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_intent', models.CharField(blank=True, max_length=255, null=True)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
    ]

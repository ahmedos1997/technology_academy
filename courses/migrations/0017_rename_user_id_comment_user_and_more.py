# Generated by Django 4.2 on 2023-10-30 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_remove_payment_stripe_payment_payment_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='replie',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='path',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
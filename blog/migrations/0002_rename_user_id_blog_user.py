# Generated by Django 4.2 on 2023-10-30 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='user_id',
            new_name='user',
        ),
    ]

# Generated by Django 4.2 on 2023-11-07 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0024_course_session'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transaction',
        ),
        migrations.RemoveField(
            model_name='course',
            name='description',
        ),
        migrations.RemoveField(
            model_name='course',
            name='session',
        ),
        migrations.AlterField(
            model_name='course',
            name='price',
            field=models.IntegerField(),
        ),
    ]

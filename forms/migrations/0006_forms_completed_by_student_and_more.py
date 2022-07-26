# Generated by Django 4.0.3 on 2022-05-01 06:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0005_remove_forms_anything'),
    ]

    operations = [
        migrations.AddField(
            model_name='forms',
            name='completed_by_student',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='forms',
            name='time_completed_by_coordinator',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 6, 3, 41, 432084)),
        ),
        migrations.AddField(
            model_name='forms',
            name='time_completed_by_student',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 6, 3, 41, 432345)),
        ),
        migrations.AddField(
            model_name='forms',
            name='time_completed_by_supervisor',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 1, 6, 3, 41, 432124)),
        ),
    ]

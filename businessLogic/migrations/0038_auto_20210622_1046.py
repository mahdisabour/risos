# Generated by Django 3.1.7 on 2021-06-22 10:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0037_auto_20210622_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='actual_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 20, 10, 46, 24, 643717), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 21, 10, 46, 24, 643666), null=True),
        ),
    ]

# Generated by Django 3.1.7 on 2021-06-20 13:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0007_auto_20210620_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='actual_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 18, 13, 16, 41, 3985), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 19, 13, 16, 41, 3919), null=True),
        ),
    ]
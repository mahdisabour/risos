# Generated by Django 3.1.7 on 2021-06-20 13:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0018_auto_20210620_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='actual_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 18, 13, 37, 2, 175974), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 19, 13, 37, 2, 175919), null=True),
        ),
    ]
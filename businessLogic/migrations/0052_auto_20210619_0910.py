# Generated by Django 3.1.7 on 2021-06-19 09:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0051_auto_20210619_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='actual_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 17, 9, 9, 59, 792237), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 18, 9, 9, 59, 792195), null=True),
        ),
    ]

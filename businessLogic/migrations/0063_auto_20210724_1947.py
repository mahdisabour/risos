# Generated by Django 3.1.7 on 2021-07-24 19:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0062_auto_20210724_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='actual_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 22, 19, 47, 7, 691873), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 22, 19, 47, 7, 691822), null=True),
        ),
    ]
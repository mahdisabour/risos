# Generated by Django 3.1.7 on 2021-07-22 08:27

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0054_auto_20210722_0729'),
    ]

    operations = [
        migrations.AddField(
            model_name='tooth',
            name='cl',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='order',
            name='actual_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 20, 8, 27, 29, 921071), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 20, 8, 27, 29, 921026), null=True),
        ),
    ]

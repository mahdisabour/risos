# Generated by Django 3.1.7 on 2021-06-22 11:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0039_auto_20210622_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='actual_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 20, 11, 27, 32, 801972), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 21, 11, 27, 32, 801926), null=True),
        ),
    ]

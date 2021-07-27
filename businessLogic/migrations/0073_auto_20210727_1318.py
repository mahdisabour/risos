# Generated by Django 3.1.7 on 2021-07-27 13:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0072_auto_20210727_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='central_size',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='actual_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 25, 13, 18, 15, 630365), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 25, 13, 18, 15, 630312), null=True),
        ),
    ]

# Generated by Django 3.1.7 on 2021-06-01 09:13

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0016_auto_20210526_0947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='patientpic',
            name='patient',
        ),
        migrations.AddField(
            model_name='patient',
            name='patient_pic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='businessLogic.patientpic'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='related_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='businessLogic.order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='actual_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 30, 9, 13, 10, 545583), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 31, 9, 13, 10, 545534), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='related_service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='businessLogic.service'),
        ),
        migrations.AlterField(
            model_name='service',
            name='related_doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='businessLogic.doctor'),
        ),
    ]

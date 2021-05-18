# Generated by Django 3.1.7 on 2021-05-18 09:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0006_auto_20210515_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='actual_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 16, 9, 1, 31, 830833), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='expected_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 17, 9, 1, 31, 830782), null=True),
        ),
        migrations.CreateModel(
            name='PatientPic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('full_smile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('side_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('optional_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patientPics', to='businessLogic.patient')),
            ],
        ),
    ]

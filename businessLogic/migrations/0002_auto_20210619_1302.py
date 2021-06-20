# Generated by Django 3.1.7 on 2021-06-19 13:02

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BadColorReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatientPic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('smile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('full_smile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('side_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('optional_image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ToothSevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='name',
        ),
        migrations.RemoveField(
            model_name='lab',
            name='name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='name',
        ),
        migrations.AddField(
            model_name='lab',
            name='rating',
            field=models.FloatField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='rating',
            field=models.FloatField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='service',
            name='related_doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='businessLogic.doctor'),
        ),
        migrations.CreateModel(
            name='Tooth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('tooth_number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(18), django.core.validators.MaxValueValidator(48)])),
                ('is_bad_color', models.BooleanField(default=False)),
                ('bad_color_reason', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='businessLogic.badcolorreason')),
                ('related_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Teeth', to='businessLogic.service')),
                ('tooth_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='businessLogic.toothsevice')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('expected_date', models.DateTimeField(blank=True, default=datetime.datetime(2021, 8, 18, 13, 2, 55, 30622), null=True)),
                ('actual_date', models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 17, 13, 2, 55, 30667), null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(choices=[('processing', 'Processing'), ('delayed', 'Delayed'), ('sent', 'Sent'), ('underdevelopment', 'Under Development'), ('finalized', 'Finalized'), ('cancelled', 'Cancelled')], default='processing', max_length=20)),
                ('finalized_lab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='businessLogic.lab')),
                ('related_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='businessLogic.service')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('expected_date', models.DateTimeField(blank=True, null=True)),
                ('actual_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(choices=[('processing', 'Processing'), ('finalized', 'Finalized'), ('cancelled', 'Cancelled')], default='processing', max_length=20)),
                ('reciept_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('related_lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='businessLogic.lab')),
                ('related_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='businessLogic.order')),
                ('related_service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='businessLogic.service')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='patient_pic',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='businessLogic.patientpic'),
        ),
        migrations.CreateModel(
            name='LabPic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('pic', models.ImageField(blank=True, null=True, upload_to='labpics/')),
                ('number', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)])),
                ('lab', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='labPics', to='businessLogic.lab')),
            ],
            options={
                'unique_together': {('lab', 'number')},
            },
        ),
    ]

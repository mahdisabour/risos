# Generated by Django 3.1.7 on 2021-06-22 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('extendProfile', '0002_auto_20210619_1302'),
        ('notification', '0023_auto_20210622_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(choices=[('order completed', 'Order Completed')], max_length=250),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[('success', 'SUCCESS'), ('failed', 'FAILED')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='notifreceiver',
            name='profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='extendProfile.profile'),
        ),
    ]
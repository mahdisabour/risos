# Generated by Django 3.1.7 on 2021-06-22 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0025_auto_20210622_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(choices=[('order updated', 'Order Updated'), ('order completed', 'Order Completed')], max_length=250),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[('failed', 'FAILED'), ('success', 'SUCCESS')], max_length=10, null=True),
        ),
    ]
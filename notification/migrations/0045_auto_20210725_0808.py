# Generated by Django 3.1.7 on 2021-07-25 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0044_auto_20210724_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(choices=[('order completed', 'Order Completed'), ('order updated', 'Order Updated')], max_length=250),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[('failed', 'FAILED'), ('success', 'SUCCESS')], max_length=10, null=True),
        ),
    ]

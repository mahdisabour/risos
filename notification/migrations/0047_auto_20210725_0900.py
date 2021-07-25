# Generated by Django 3.1.7 on 2021-07-25 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0046_auto_20210725_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(choices=[('order completed', 'Order Completed'), ('order updated', 'Order Updated')], max_length=250),
        ),
        migrations.AlterField(
            model_name='notifservice',
            name='object_type',
            field=models.CharField(choices=[('order', 'ORDER'), ('invoice', 'INVOICE')], max_length=50),
        ),
    ]
# Generated by Django 3.1.7 on 2021-06-22 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0024_auto_20210622_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(choices=[('order completed', 'Order Completed'), ('order updated', 'Order Updated')], max_length=250),
        ),
    ]

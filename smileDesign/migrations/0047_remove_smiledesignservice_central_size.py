# Generated by Django 3.1.7 on 2021-07-27 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smileDesign', '0046_auto_20210727_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smiledesignservice',
            name='central_size',
        ),
    ]
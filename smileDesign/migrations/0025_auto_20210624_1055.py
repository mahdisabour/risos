# Generated by Django 3.1.7 on 2021-06-24 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smileDesign', '0024_auto_20210624_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smileplot',
            name='unit',
            field=models.CharField(choices=[('px', 'Pixel'), ('cm', 'Centi Meter')], default='px', max_length=50),
        ),
    ]

# Generated by Django 3.1.7 on 2021-06-20 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smileDesign', '0011_auto_20210620_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smileplot',
            name='unit',
            field=models.CharField(choices=[('cm', 'Centi Meter'), ('px', 'Pixel')], default='px', max_length=50),
        ),
    ]
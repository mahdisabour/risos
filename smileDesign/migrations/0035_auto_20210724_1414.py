# Generated by Django 3.1.7 on 2021-07-24 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smileDesign', '0034_auto_20210722_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smileplot',
            name='unit',
            field=models.CharField(choices=[('px', 'Pixel'), ('cm', 'Centi Meter')], default='px', max_length=50),
        ),
    ]

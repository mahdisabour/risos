# Generated by Django 3.1.7 on 2021-06-21 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smileDesign', '0015_auto_20210621_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smileplot',
            name='unit',
            field=models.CharField(choices=[('cm', 'Centi Meter'), ('px', 'Pixel')], default='px', max_length=50),
        ),
    ]

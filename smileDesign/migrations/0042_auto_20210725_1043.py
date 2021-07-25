# Generated by Django 3.1.7 on 2021-07-25 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smileDesign', '0041_auto_20210725_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smiledesignservice',
            old_name='teet_less_image',
            new_name='teeth_less_image',
        ),
        migrations.AlterField(
            model_name='smileplot',
            name='unit',
            field=models.CharField(choices=[('cm', 'Centi Meter'), ('px', 'Pixel')], default='px', max_length=50),
        ),
    ]
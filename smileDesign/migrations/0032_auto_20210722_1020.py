# Generated by Django 3.1.7 on 2021-07-22 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0057_auto_20210722_1020'),
        ('smileDesign', '0031_auto_20210722_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='smiledesignservice',
            name='patient',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='businessLogic.patient'),
        ),
        migrations.AlterField(
            model_name='smileplot',
            name='unit',
            field=models.CharField(choices=[('px', 'Pixel'), ('cm', 'Centi Meter')], default='px', max_length=50),
        ),
    ]

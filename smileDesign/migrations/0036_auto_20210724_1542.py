# Generated by Django 3.1.7 on 2021-07-24 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('businessLogic', '0061_auto_20210724_1542'),
        ('smileDesign', '0035_auto_20210724_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smiledesignservice',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='businessLogic.patient'),
        ),
        migrations.AlterField(
            model_name='smileplot',
            name='unit',
            field=models.CharField(choices=[('cm', 'Centi Meter'), ('px', 'Pixel')], default='px', max_length=50),
        ),
    ]
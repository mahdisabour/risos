# Generated by Django 3.1.7 on 2021-06-19 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smileDesign', '0014_auto_20210619_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teethcoordinate',
            old_name='teeth_number',
            new_name='sequence',
        ),
        migrations.AlterField(
            model_name='rectangle',
            name='x1',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='rectangle',
            name='x2',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='rectangle',
            name='y1',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='rectangle',
            name='y2',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='smileplot',
            name='unit',
            field=models.CharField(choices=[('cm', 'Centi Meter'), ('px', 'Pixel')], default='px', max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='teethcoordinate',
            unique_together={('sequence', 'related_smile_plot')},
        ),
    ]

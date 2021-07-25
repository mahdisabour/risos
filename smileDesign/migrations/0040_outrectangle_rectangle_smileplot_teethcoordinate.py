# Generated by Django 3.1.7 on 2021-07-25 09:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smileDesign', '0039_remove_smiledesignservice_patient'),
    ]

    operations = [
        migrations.CreateModel(
            name='RectAngle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x1', models.FloatField(default=0)),
                ('y1', models.FloatField(default=0)),
                ('x2', models.FloatField(default=0)),
                ('y2', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SmilePlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('unit', models.CharField(choices=[('px', 'Pixel'), ('cm', 'Centi Meter')], default='px', max_length=50)),
                ('related_smile_design', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='smile_plot', to='smileDesign.smiledesignservice')),
            ],
        ),
        migrations.CreateModel(
            name='OutRectangle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('rect_angle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='smileDesign.rectangle')),
                ('related_smile_plot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='out_rectangle', to='smileDesign.smileplot')),
            ],
        ),
        migrations.CreateModel(
            name='TeethCoordinate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('sequence', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('rect_angle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='smileDesign.rectangle')),
                ('related_smile_plot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teeth_coordinates', to='smileDesign.smileplot')),
            ],
            options={
                'unique_together': {('sequence', 'related_smile_plot')},
            },
        ),
    ]
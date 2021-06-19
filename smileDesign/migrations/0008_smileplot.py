# Generated by Django 3.1.7 on 2021-06-19 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smileDesign', '0007_delete_smileplot'),
    ]

    operations = [
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
    ]

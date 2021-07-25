# Generated by Django 3.1.7 on 2021-07-01 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smileDesign', '0026_auto_20210624_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smileplot',
            name='unit',
            field=models.CharField(choices=[('px', 'Pixel'), ('cm', 'Centi Meter')], default='px', max_length=50),
        ),
        migrations.CreateModel(
            name='Teeth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teeth_image', models.ImageField(blank=True, null=True, upload_to='Teeth/')),
                ('related_smile_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smileDesign.smilecategory')),
                ('related_smile_color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smileDesign.smilecolor')),
            ],
        ),
    ]
# Generated by Django 3.1.7 on 2021-07-22 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0036_auto_20210715_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[('success', 'SUCCESS'), ('failed', 'FAILED')], max_length=10, null=True),
        ),
    ]
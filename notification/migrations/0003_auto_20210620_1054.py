# Generated by Django 3.1.7 on 2021-06-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20210619_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[('success', 'SUCCESS'), ('failed', 'FAILED')], max_length=10, null=True),
        ),
    ]
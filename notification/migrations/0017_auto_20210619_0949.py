# Generated by Django 3.1.7 on 2021-06-19 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0016_auto_20210619_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[('success', 'SUCCESS'), ('failed', 'FAILED')], max_length=10, null=True),
        ),
    ]

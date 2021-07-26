# Generated by Django 3.1.7 on 2021-07-26 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0049_auto_20210725_1043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='service',
            new_name='notif_service',
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[('success', 'SUCCESS'), ('failed', 'FAILED')], max_length=10, null=True),
        ),
    ]

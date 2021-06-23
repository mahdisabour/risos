# Generated by Django 3.1.7 on 2021-06-22 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('extendProfile', '0002_auto_20210619_1302'),
        ('notification', '0021_auto_20210622_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(blank=True, choices=[('success', 'SUCCESS'), ('failed', 'FAILED')], max_length=10, null=True),
        ),
        migrations.CreateModel(
            name='NotifReceiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('device_id', models.CharField(max_length=50, unique=True)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='extendProfile.profile')),
            ],
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-25 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_management', '0002_alter_log_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='level',
            field=models.CharField(max_length=10),
        ),
    ]

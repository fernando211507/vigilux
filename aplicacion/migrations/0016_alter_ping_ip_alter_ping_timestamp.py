# Generated by Django 5.1 on 2024-10-03 19:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0015_alter_ping_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ping',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='ping',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 5.1.4 on 2025-02-03 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

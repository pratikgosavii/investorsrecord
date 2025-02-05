# Generated by Django 5.1.4 on 2025-02-02 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_is_salesman'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_accounts',
            new_name='is_operator',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_cutter',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_designer',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_reception',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_salesman',
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

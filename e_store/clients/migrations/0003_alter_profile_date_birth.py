# Generated by Django 4.1.4 on 2023-01-09 09:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_profile_date_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_birth',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

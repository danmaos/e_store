# Generated by Django 4.1.5 on 2023-01-16 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_comment_date_alter_review_date_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='sale',
            field=models.BooleanField(default=False),
        ),
    ]

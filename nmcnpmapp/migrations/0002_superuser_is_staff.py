# Generated by Django 5.1.3 on 2024-11-12 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nmcnpmapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='superuser',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]

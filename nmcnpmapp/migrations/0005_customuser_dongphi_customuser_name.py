# Generated by Django 4.2.7 on 2023-11-06 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nmcnpmapp', '0004_remove_familymember_group_names_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='dongphi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]

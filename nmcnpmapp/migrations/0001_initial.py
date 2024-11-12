# Generated by Django 5.1.3 on 2024-11-12 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SuperUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.CharField(max_length=255)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('room_id', models.CharField(max_length=100, unique=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('registry_email', models.EmailField(default='example@gmail.com', max_length=254)),
                ('phone_number', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='nmcnpmapp.payment')),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_statuses', to='nmcnpmapp.roomuser', to_field='room_id')),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.PositiveIntegerField(default=13)),
                ('email', models.EmailField(default='lol@gmail.com', max_length=254)),
                ('phone_number', models.CharField(default='0123456789', max_length=10)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_members', to='nmcnpmapp.roomuser', to_field='room_id')),
            ],
        ),
    ]

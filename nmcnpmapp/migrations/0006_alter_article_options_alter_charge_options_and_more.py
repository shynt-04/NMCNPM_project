# Generated by Django 5.1.3 on 2024-11-27 03:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nmcnpmapp', '0005_alter_charge_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Quản lý thông báo', 'verbose_name_plural': 'Quản lý thông báo'},
        ),
        migrations.AlterModelOptions(
            name='charge',
            options={'verbose_name': 'Quản lý khoản thu', 'verbose_name_plural': 'Quản lý khoản thu'},
        ),
        migrations.AlterModelOptions(
            name='familymember',
            options={'verbose_name': 'Quản lý nhân khẩu', 'verbose_name_plural': 'Quản lý nhân khẩu'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Quản lý khoản thanh toán', 'verbose_name_plural': 'Quản lý khoản thanh toán'},
        ),
        migrations.AlterModelOptions(
            name='roomuser',
            options={'verbose_name': 'Quản lý tài khoản', 'verbose_name_plural': 'Quản lý tài khoản'},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'verbose_name': 'Quản lý gửi xe', 'verbose_name_plural': 'Quản lý gửi xe'},
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(verbose_name='Nội dung'),
        ),
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Ngày đăng'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Tiêu đề'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='category',
            field=models.CharField(choices=[('Tiền điện', 'Tiền điện'), ('Tiền nước', 'Tiền nước'), ('Phí dịch vụ', 'Phí dịch vụ'), ('Phí quản lý', 'Phí quản lý'), ('Phí gửi xe', 'Phí gửi xe'), ('Khác', 'Khác')], default='Khác', max_length=50, verbose_name='Loại khoản thu'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='charge_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Mã khoản thu'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='create_at',
            field=models.DateField(auto_now_add=True, verbose_name='Ngày tạo'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='create_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charges', to=settings.AUTH_USER_MODEL, verbose_name='Người tạo'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='deadline',
            field=models.DateField(verbose_name='Hạn thanh toán'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Tên khoản thu'),
        ),
        migrations.AlterField(
            model_name='charge',
            name='target_room',
            field=models.ManyToManyField(related_name='charges', to='nmcnpmapp.apartment', verbose_name='Đối tượng thu'),
        ),
        migrations.AlterField(
            model_name='familymember',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Ngày sinh'),
        ),
        migrations.AlterField(
            model_name='familymember',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='Họ'),
        ),
        migrations.AlterField(
            model_name='familymember',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Tên'),
        ),
        migrations.AlterField(
            model_name='familymember',
            name='phone_number',
            field=models.CharField(default='0123456789', max_length=10, verbose_name='Số điện thoại'),
        ),
        migrations.AlterField(
            model_name='familymember',
            name='room_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='family_members', to='nmcnpmapp.apartment', verbose_name='Số phòng'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='Số tiền'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='charge_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='nmcnpmapp.charge', verbose_name='Mã khoản thu'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Ngày tạo'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Mã thanh toán'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='room_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='nmcnpmapp.apartment', verbose_name='Số phòng'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Trạng thái'),
        ),
        migrations.AlterField(
            model_name='roomuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Kích hoạt'),
        ),
        migrations.AlterField(
            model_name='roomuser',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Trạng thái'),
        ),
        migrations.AlterField(
            model_name='roomuser',
            name='phone_number',
            field=models.CharField(max_length=10, unique=True, verbose_name='Số điện thoại'),
        ),
        migrations.AlterField(
            model_name='roomuser',
            name='registry_email',
            field=models.EmailField(default='example@gmail.com', max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='roomuser',
            name='room_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='nmcnpmapp.apartment', verbose_name='Số phòng'),
        ),
        migrations.AlterField(
            model_name='roomuser',
            name='username',
            field=models.CharField(max_length=100, unique=True, verbose_name='Tên tài khoản'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='license_plate',
            field=models.CharField(max_length=30, verbose_name='Biển số xe'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='room_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='nmcnpmapp.apartment', verbose_name='Số phòng'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='type_vehicle',
            field=models.IntegerField(choices=[(1, 'Xe đạp'), (2, 'Xe máy'), (3, 'Ô tô')], verbose_name='Loại xe'),
        ),
    ]

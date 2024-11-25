#models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.db import models

class RoomUserManager(BaseUserManager):
    def create_user(self, room_id, username, registry_email, password=None, **extra_fields):
        if not room_id:
            raise ValueError("The Room ID field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        if not registry_email:
            raise ValueError("The Email field must be set")
        
        if RoomUser.objects.filter(room_id=room_id).exists():
            raise ValueError("Room ID already exists")
        if RoomUser.objects.filter(username=username).exists():
            raise ValueError("Username already exists")
        
        registry_email = self.normalize_email(registry_email)
        user = self.model(room_id=room_id, username=username, registry_email=registry_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class SuperUserManager(BaseUserManager):
    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class SuperUser(AbstractBaseUser, PermissionsMixin):  # Add PermissionsMixin here
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    # The is_superuser field is inherited from PermissionsMixin

    objects = SuperUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
class apartment(models.Model):
    room_id = models.IntegerField(primary_key=True)
    area = models.IntegerField(default =0)
    def __str__(self) -> str:
        return f"Phòng {self.room_id}"
# RoomUser Model
class RoomUser(AbstractBaseUser):
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE,related_name="user",verbose_name="Số phòng")
    username = models.CharField(max_length=100, unique=True,verbose_name="Tên tài khoản")
    registry_email = models.EmailField(default="example@gmail.com",verbose_name="Email")
    phone_number = models.CharField(max_length=10, unique=True,verbose_name="Số điện thoại")
    is_approved = models.BooleanField(default=False,verbose_name="Trạng thái")
    is_active = models.BooleanField(default=True,verbose_name="Kích hoạt")

    objects = RoomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['room_id', 'registry_email', 'phone_number']

    def __str__(self):
        return self.username
    class Meta:
        verbose_name = "Quản lý tài khoản"
        verbose_name_plural = "Quản lý tài khoản"

class Vehicle(models.Model):
    '''
    type_vehicle: 1:xe đạp, 2: xe máy, 3: ô tô
    '''
    CATEGORY_CHOICES = [
        (1, "Xe đạp"),
        (2, "Xe máy"),
        (3, "Ô tô"),
    ]
    license_plate = models.CharField(max_length=30,verbose_name="Biển số xe")
    type_vehicle = models.IntegerField(choices=CATEGORY_CHOICES,verbose_name="Loại xe")
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE, related_name="vehicles",verbose_name='Số phòng')
    class Meta:
        verbose_name = "Quản lý gửi xe"
        verbose_name_plural = "Quản lý gửi xe"
    
class Charge(models.Model):
    # trường thứ nhất trong category_choices sẽ là giá trị lưu trong database, 
    # trường thứ hai sẽ là giá trị hiển thị trên giao diện
    CATEGORY_CHOICES = [
    ("Tiền điện", "Tiền điện"),
    ("Tiền nước", "Tiền nước"),
    ("Phí dịch vụ", "Phí dịch vụ"),
    ("Phí quản lý", "Phí quản lý"),
    ("Phí gửi xe", "Phí gửi xe"),
    ("Khác", "Khác"),
    ]
    charge_id = models.AutoField(primary_key=True,verbose_name="Mã khoản thu")
    name = models.CharField(max_length=255,verbose_name="Tên khoản thu")
    create_at = models.DateField(auto_now_add=True,verbose_name="Ngày tạo")
    create_by = models.ForeignKey(SuperUser,on_delete = models.CASCADE, related_name="charges",verbose_name="Người tạo")
    deadline = models.DateField(verbose_name="Hạn thanh toán")
    target_room = models.ManyToManyField(apartment, related_name="charges",verbose_name="Đối tượng thu")  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Khác",verbose_name="Loại khoản thu")
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Quản lý khoản thu"
        verbose_name_plural = "Quản lý khoản thu"
# Store payment details
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True,verbose_name="Mã thanh toán")
    charge_id = models.ForeignKey(Charge, on_delete=models.CASCADE, related_name="payments",verbose_name="Mã khoản thu")
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE, related_name="payments",verbose_name="Số phòng")
    amount = models.PositiveIntegerField(verbose_name="Số tiền")
    date = models.DateField(auto_now_add=True,verbose_name="Ngày tạo")
    status = models.BooleanField(default=False,verbose_name="Trạng thái")
    class Meta:
        verbose_name = "Quản lý khoản thanh toán"
        verbose_name_plural = "Quản lý khoản thanh toán"
    def __str__(self):
        return f"Mã thanh toán {self.payment_id}"

# Store family members details
class FamilyMember(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE, related_name="family_members",verbose_name="Số phòng")
    first_name = models.CharField(max_length=50,verbose_name="Họ")
    last_name = models.CharField(max_length=50,verbose_name="Tên")
    date_of_birth = models.DateField(null=True, blank=True,verbose_name="Ngày sinh")
    email = models.EmailField(default="lol@gmail.com")
    phone_number = models.CharField(max_length=10, default="0123456789",verbose_name="Số điện thoại")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        verbose_name = "Quản lý nhân khẩu"
        verbose_name_plural = "Quản lý nhân khẩu"

# Store notification details
class Article(models.Model):
    title = models.CharField(max_length=255,verbose_name="Tiêu đề")
    content = models.TextField(verbose_name="Nội dung")
    date = models.DateField(auto_now_add=True,verbose_name="Ngày đăng")
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Quản lý thông báo"
        verbose_name_plural = "Quản lý thông báo"

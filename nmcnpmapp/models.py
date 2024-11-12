from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class RoomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)

class RoomUser(AbstractBaseUser, PermissionsMixin):
    room_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    is_approved = models.BooleanField(default=False)
    registry_email = models.EmailField(default="example@gmail.com")
    phone_number = models.CharField(max_length=10, default="0123456789")
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['room_id', 'registry_email', 'phone_number']

    objects = RoomUserManager()

    def __str__(self):
        return self.username

# Store payment details
class Payment(models.Model):
    payment = models.CharField(max_length=255)
    amount = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment} - {self.amount}"

# Table to store payment status of each room
class PaymentStatus(models.Model):
    room_id = models.ForeignKey(RoomUser, on_delete=models.CASCADE, to_field='room_id', related_name="payment_statuses")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="statuses")
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.room_id.room_id} - {self.payment.payment} - {self.status}"

# Store family members details
class FamilyMember(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(RoomUser, on_delete=models.CASCADE, to_field='room_id', related_name="family_members")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=13)
    email = models.EmailField(default="lol@gmail.com")
    phone_number = models.CharField(max_length=10, default="0123456789")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Store notification details
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title

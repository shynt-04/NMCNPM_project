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
# RoomUser Model
class RoomUser(AbstractBaseUser):
    room_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    registry_email = models.EmailField(default="example@gmail.com")
    phone_number = models.CharField(max_length=10, unique=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = RoomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['room_id', 'registry_email', 'phone_number']

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

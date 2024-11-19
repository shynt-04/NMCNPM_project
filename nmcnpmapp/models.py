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
# RoomUser Model
class RoomUser(AbstractBaseUser):
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE,related_name="user")
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

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=30)
    type_vehicle = models.IntegerField()
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE, related_name="vehicles")
    
class Charge(models.Model):
    charge_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    create_at = models.DateField(auto_now_add=True)
    create_by = models.ForeignKey(SuperUser,on_delete = models.CASCADE, related_name="charges")
    deadline = models.DateField()
    target_room = models.ManyToManyField(apartment, related_name="charges")  
    
# Store payment details
class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    charge_id = models.ForeignKey(Charge, on_delete=models.CASCADE, related_name="payments")
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE, related_name="payments")
    amount = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

# Store family members details
class FamilyMember(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(apartment, on_delete=models.CASCADE, related_name="family_members")
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

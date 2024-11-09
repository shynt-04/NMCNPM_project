from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(models.Model):
    room_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    registry_email = models.EmailField(default="lol@gamil.com")
    phone_number = models.CharField(max_length=10, default="0123456789")

    def __str__(self):
        return self.username
#Store payment details
class Payment(models.Model):
    payment = models.CharField(max_length=255)
    amount = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment} - {self.amount}"

#Table to store payment status of each room
class PaymentStatus(models.Model):
    room_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='room_id', related_name="payment_statuses")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="statuses")
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.room_id.room_id} - {self.payment.payment} - {self.status}"
#Store family members details
class FamilyMember(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='room_id', related_name="family_members")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=13)
    email = models.EmailField(default="lol@gamil.com")
    phone_number = models.CharField(max_length=10, default="0123456789")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
#Store notification details
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='article_images/')
    link = models.URLField()

    def __str__(self):
        return self.title

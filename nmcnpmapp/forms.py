from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('room_id', 'username', 'registry_email', 'phone_number')

class CustomAuthenticationForm(AuthenticationForm):
    # Meta class removed for simplicity
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

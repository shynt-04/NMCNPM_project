from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import RoomUser
from django.contrib.auth import authenticate

# Custom form for creating RoomUser accounts
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = RoomUser
        fields = ('username', 'password1', 'password2', 'room_id', 'registry_email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom placeholders or widget settings if needed
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})
        self.fields['room_id'].widget.attrs.update({'placeholder': 'Room ID'})
        self.fields['registry_email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Phone number'})

# Custom form for authenticating RoomUser accounts
class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    user = None  # Store the authenticated user instance if successful

    def clean(self):
        # Retrieve the cleaned data
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        
        # Try to authenticate the user using Django's authenticate function
        user = authenticate(username=username, password=password)
        
        if user is None:
            # User could not be authenticated
            raise forms.ValidationError("Invalid username or password.")
        
        if hasattr(user, 'is_approved') and not user.is_approved:
            # If the user is a RoomUser and not approved
            raise forms.ValidationError("Your account is awaiting approval.")
        
        # Store the authenticated user in the form
        self.user = user
        return cleaned_data

    def get_user(self):
        return self.user
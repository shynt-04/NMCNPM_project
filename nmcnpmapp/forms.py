from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import RoomUser,Charge,Payment,apartment
from django.contrib.auth import authenticate
import pandas as pd 
from django.core.exceptions import ValidationError

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
    
class ChargeForm(forms.ModelForm):
    excel_file = forms.FileField(
        required=False, 
        label="Tải lên file Excel"
    )

    class Meta:
        model = Charge
        fields = ['name', 'create_by', 'deadline', 'target_room']

    def clean_excel_file(self):
        file = self.cleaned_data.get('excel_file')
        if file and not file.name.endswith(('.xls', '.xlsx')):
            raise ValidationError("File phải có định dạng .xls hoặc .xlsx")
        return file

    def process_excel_file(self, excel_file, charge_instance):
        """
        Đọc dữ liệu từ file Excel và tạo các bản ghi Payment.
        """
        try:
            # Đọc dữ liệu từ file Excel
            df = pd.read_excel(excel_file)

            # Kiểm tra các cột cần thiết
            if 'Số nhà' not in df.columns or 'Số tiền' not in df.columns:
                raise ValidationError("File Excel cần có các cột: 'Số nhà', 'Số tiền'")

            # Tạo các bản ghi Payment
            payments_created = []
            for _, row in df.iterrows():
                room_id = row['Số nhà']
                amount = row['Số tiền']

                # Tìm phòng
                room = apartment.objects.filter(room_id=room_id).first()
                if not room:
                    raise ValidationError(f"Không tìm thấy phòng với ID {room_id}")

                # Tạo Payment
                payment = Payment.objects.create(
                    charge_id=charge_instance,
                    room_id=room,
                    amount=amount,
                )
                payments_created.append(payment)
            return payments_created
        except Exception as e:
            raise ValidationError(f"Lỗi xử lý file Excel: {e}")
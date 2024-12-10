#forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import RoomUser,Charge,Payment,apartment,Vehicle, Notification
from . import models
from django.contrib.auth import authenticate
import pandas as pd 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Custom form for creating RoomUser accounts
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = RoomUser
        fields = ('username', 'password1', 'password2', 'room_id', 'registry_email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom placeholders or widget settings if needed
        self.fields['username'].widget.attrs.update({'placeholder': 'Tên đăng nhập'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Mật khẩu'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Nhập lại mật khẩu'})
        self.fields['room_id'].widget.attrs.update({'placeholder': 'Số hiệu phòng'})
        self.fields['registry_email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Số điện thoại'})

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
        
        # Store the authenticated user in the form
        self.user = user
        return cleaned_data

    def get_user(self):
        return self.user
    
class ChargeForm(forms.ModelForm):
    excel_file = forms.FileField(
        required=False, 
        label="Tải lên file Excel",
        help_text="Chỉ áp dụng cho Tiền điện/Tiền nước."
    )
    unit_price = forms.DecimalField(
        required=False, 
        max_digits=10, 
        decimal_places=3, 
        label="Đơn giá (VNĐ/m2)",
        help_text="Chỉ áp dụng cho Phí dịch vụ/Phí quản lý."
    )
    CATEGORY_CHOICES = [
    ("Tiền điện", "Tiền điện"),
    ("Tiền nước", "Tiền nước"),
    ("Phí dịch vụ", "Phí dịch vụ"),
    ("Phí quản lý", "Phí quản lý"),
    ("Phí gửi xe", "Phí gửi xe"),
    ("Khác", "Khác"),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label="Loại khoản thu")
    
    class Meta:
        model = Charge
        fields = ['category','name', 'create_by', 'deadline']

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        excel_file = cleaned_data.get("excel_file")
        unit_price = cleaned_data.get("unit_price")

        # Kiểm tra điều kiện theo loại khoản thu
        if category in ["Tiền điện", "Tiền nước"]:
            cleaned_data["unit_price"] = None
            if not excel_file:
                raise forms.ValidationError("Vui lòng tải lên file Excel cho Tiền điện/Tiền nước.")
        elif category in ["Phí dịch vụ", "Phí quản lý"]:
            if not unit_price:
                raise forms.ValidationError("Vui lòng nhập đơn giá cho Phí dịch vụ/Phí quản lý.")            
            cleaned_data["excel_file"] = None
        elif category == "Phí gửi xe":
            cleaned_data["unit_price"] = None
            cleaned_data["excel_file"] = None
        elif category == "Khác":
            cleaned_data["unit_price"] = None
            cleaned_data["excel_file"] = None
        return cleaned_data

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
            target_residents = []
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
                target_residents.append(room)
            return target_residents
        except Exception as e:
            raise ValidationError(f"Lỗi xử lý file Excel: {e}")
    def calculate_service_fee(self, unit_price, charge_instance):
        """
        Tính toán amount = đơn giá * diện tích cho Phí dịch vụ/Phí quản lý.
        """
        payments = []
        rooms = apartment.objects.all()
        for room in rooms:
            amount = unit_price * room.area
            payments.append(Payment(
                charge_id=charge_instance,
                room_id=room,
                amount=amount
            ))
        Payment.objects.bulk_create(payments)
        return payments
    def calculate_parking_fee(self, charge_instance):

        payments = []
        vehicles = Vehicle.objects.all()
        for vehicle in vehicles:
            payments.append(Payment(
                charge_id=charge_instance,
                room_id=vehicle.room_id,
                amount=50 if vehicle.type_vehicle == 0 else 100 if vehicle.type_vehicle == 1 else 300
            ))
        Payment.objects.bulk_create(payments)


#form add thông báo cho từng hộ custom cho admin
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'content', 'room_id']

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        
        # Set the queryset for the room_id field to only rooms with approved users
        self.fields['room_id'].queryset = RoomUser.objects.filter(is_approved=True).values_list('room_id', flat=True).distinct()

    def clean_room_id(self):
        room_id = self.cleaned_data.get('room_id')
        
        # Check if there are any approved users in the room
        if not RoomUser.objects.filter(room_id=room_id, is_approved=True).exists():
            raise forms.ValidationError("Phòng này không có người được duyệt nên không thể thêm thông báo !!!")
        
        # Retrieve the actual 'apartment' instance corresponding to room_id
        apartment_instance = apartment.objects.get(room_id=room_id)
        
        # Return the apartment instance to be assigned to the Notification model
        return apartment_instance


#form add bill cho từng hộ custom cho admin

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['room_id', 'charge_id', 'amount', 'status']

    room_id = forms.ModelChoiceField(queryset=apartment.objects.none(), label=_('Số phòng'))  # Initially empty queryset
    charge_id = forms.ModelChoiceField(queryset=Charge.objects.all(), label=_('Khoản thu'))
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label=_('Số tiền'))
    status = forms.ChoiceField(choices=[(True, 'Đã thanh toán'), (False, 'Chưa thanh toán')], label=_('Trạng thái'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter rooms that have users associated with them
        self.fields['room_id'].queryset = RoomUser.objects.filter(is_approved=True).values_list('room_id', flat=True).distinct()

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room_id')

        # Check if the selected room is valid (it should always be, as the queryset is filtered)
        if room and not RoomUser.objects.filter(room_id=room).exists():
            raise ValidationError(_("Cannot create payment because there are no users in this room."))

        return cleaned_data

class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'style': 'width: 80%;min-height: 40px',
            }),
            'content': forms.Textarea(attrs={
                'style': 'width: 80%; min-height: 200px;',  # Tăng chiều rộng và chiều cao
            }),
        }
        
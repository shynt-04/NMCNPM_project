# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Payment, Charge, FamilyMember, Article, RoomUser, SuperUser,apartment, Vehicle, Notification
from .forms import ChargeForm, PaymentForm, NotificationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
admin.site.site_header = "Chung cư Blue Moon"
admin.site.site_title = "Quản lý chung cư"
admin.site.index_title = "Các chức năng"
# Register the Article model
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date')
    search_fields = ('title', 'author')
    list_filter = ('date',)
    readonly_fields = ('date',)
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý thông báo")
        return super().changelist_view(request, extra_context=extra_context)
admin.site.register(Article, ArticleAdmin)

# Customized admin for RoomUser
@admin.register(RoomUser)
class RoomUser(admin.ModelAdmin):
    list_display = ['username', 'room_id', 'registry_email','phone_number','is_approved']
    search_fields = ['username', 'room_id', 'registry_email','phone_number','is_approved']
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý tài khoản")
        return super().changelist_view(request, extra_context=extra_context)
# @admin.register(SuperUser)
# class SuperUserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'email','password']
#     search_fields = ['username', 'email']

# Register other models
class ChargeAdmin(admin.ModelAdmin):
    form = ChargeForm
    list_display = ('category','name', 'create_at', 'create_by', 'deadline')
    search_fields = ('name','category','create_by__username')
    list_filter = ('category','create_at', 'deadline' )
    # tạo title cho header
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý khoản thu")
        return super().changelist_view(request, extra_context=extra_context)
    
    # save charge into database
    def save_model(self, request, obj, form, change):
        # Lưu Charge trước
        super().save_model(request, obj, form, change)

        category = form.cleaned_data.get("category")
        excel_file = form.cleaned_data.get("excel_file")
        unit_price = form.cleaned_data.get("unit_price")

        if category in ["Tiền điện", "Tiền nước"] and excel_file:
            # Xử lý file Excel
            try:
                target_residents = form.process_excel_file(excel_file, obj)
                # Thêm các target_room vào charge
                obj.target_room.set(target_residents)
                obj.save()
            except ValidationError as e:
                raise ValidationError(f"Lỗi khi xử lý file Excel: {e}")
        elif category in ["Phí dịch vụ", "Phí quản lý"] and unit_price:
            # Tính toán amount từ đơn giá
            form.calculate_service_fee(unit_price, obj)
            # Thêm các target_room vào charge
            target_residents = apartment.objects.values_list('room_id', flat=True)
            obj.target_room.set(target_residents)
            obj.save()
        elif category == "Phí gửi xe":
            form.calculate_parking_fee(obj)
            # Thêm các target_room vào charge
            target_residents = Vehicle.objects.values_list('room_id', flat=True).distinct()
            obj.target_room.set(target_residents)
            obj.save()
            
            
admin.site.register(Charge,ChargeAdmin)
class VehicleIn4(admin.ModelAdmin):
    list_display = ('room_id', 'license_plate', 'type_vehicle')
    search_fields = ('license_plate', 'type_vehicle', 'room_id')
    list_filter = ('type_vehicle','room_id')
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý gửi xe")
        return super().changelist_view(request, extra_context=extra_context)
admin.site.register(Vehicle,VehicleIn4)

class PaymentIn4(admin.ModelAdmin):
    form = PaymentForm
    list_display = ('room_id', 'get_charge_name', 'amount','date','status')
    search_fields = ('room_id__room_id', 'charge_id__name','status')
    list_filter = ('status','charge_id__name','room_id')
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý thanh toán")
        return super().changelist_view(request, extra_context=extra_context)
    # Tùy chỉnh hiển thị cột
    @admin.display(description='Tên khoản thu')  # Đổi nhãn cột
    def get_charge_name(self, obj):
        return obj.charge_id.name  # Truy cập trường name từ ForeignKey charge_id
    # def display_status(self, obj):
    #     return "Đã thanh toán" if obj.status else "Chưa thanh toán"
admin.site.register(Payment,PaymentIn4)

class ApartIn4(admin.ModelAdmin):
    list_display = ('room_id', 'area')
    search_fields = ('room_id', 'area')
# admin.site.register(apartment,ApartIn4)
class FamilyMemberAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin
    list_display = ('room_id', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('room_id',)
    readonly_fields = ('room_id',)
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý nhân khẩu")
        return super().changelist_view(request, extra_context=extra_context)
    # Organize fields into sections in the detail view
    fieldsets = (
        (None, {
            'fields': ('room_id', 'first_name', 'last_name', 'date_of_birth')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_number')
        }),
    )

# Register the custom admin class with the FamilyMember model
admin.site.register(FamilyMember, FamilyMemberAdmin)


class NotiIn4(admin.ModelAdmin):
    form = NotificationForm
    list_display = ('title', 'content', 'room_id')
    search_fields = ('title', 'author','room_id')
    list_filter = ('date','room_id')
   
    # Tùy chỉnh title
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = _("Quản lý thông báo")
        return super().changelist_view(request, extra_context=extra_context)
admin.site.register(Notification,NotiIn4)

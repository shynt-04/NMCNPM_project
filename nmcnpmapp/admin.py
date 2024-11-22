# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Payment, Charge, FamilyMember, Article, RoomUser, SuperUser,apartment
from .forms import ChargeForm
from django.core.exceptions import ValidationError

# Register the Article model
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date')
    search_fields = ('title', 'author')
    list_filter = ('date',)
    readonly_fields = ('date',)

admin.site.register(Article, ArticleAdmin)

# Customized admin for RoomUser
@admin.register(RoomUser)
class RoomUser(admin.ModelAdmin):
    list_display = ['username', 'room_id', 'registry_email','phone_number','is_approved']
    search_fields = ['username', 'room_id', 'registry_email','phone_number','is_approved']

@admin.register(SuperUser)
class SuperUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','password']
    search_fields = ['username', 'email']

# Register other models
class ChargeAdmin(admin.ModelAdmin):
    form = ChargeForm
    list_display = ('category','name', 'create_at', 'create_by', 'deadline')
    search_fields = ('name',)
    list_filter = ('category','create_at', 'deadline' )
    readonly_fields = ('create_at',) # chỉ định trường thông thể chỉnh sửa

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
            
admin.site.register(Charge,ChargeAdmin)
class PaymentIn4(admin.ModelAdmin):
    list_display = ('room_id', 'charge_id__name', 'amount','date','status')
    search_fields = ('room_id', 'charge_id__name','status')
    list_filter = ('room_id','charge_id__name','status')
admin.site.register(Payment,PaymentIn4)
class ApartIn4(admin.ModelAdmin):
    list_display = ('room_id', 'area')
    search_fields = ('room_id', 'area')
admin.site.register(apartment,ApartIn4)
class FamilyMemberAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin
    list_display = ('room_id', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone_number')
    
    # Add search functionality for these fields
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    
    # Allow filtering by room ID
    list_filter = ('room_id',)
    
    # Specify read-only fields, if applicable
    readonly_fields = ('room_id',)
    
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

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
    list_display = ('name', 'create_at', 'create_by', 'deadline')
    search_fields = ('name',)
    list_filter = ('create_at', 'deadline')
    readonly_fields = ('create_at',) # chỉ định trường thông thể chỉnh sửa

    def save_model(self, request, obj, form, change):
        # Lưu Charge trước
        super().save_model(request, obj, form, change)

        # Xử lý file Excel nếu được tải lên
        excel_file = form.cleaned_data.get('excel_file')
        if excel_file:
            try:
                form.process_excel_file(excel_file, obj)
            except ValidationError as e:
                raise ValidationError(f"Lỗi khi tạo các bản ghi Payment: {e}")
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
    list_display = ('room_id', 'first_name', 'last_name', 'age', 'email', 'phone_number')
    
    # Add search functionality for these fields
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    
    # Allow filtering by room ID
    list_filter = ('room_id',)
    
    # Specify read-only fields, if applicable
    readonly_fields = ('room_id',)
    
    # Organize fields into sections in the detail view
    fieldsets = (
        (None, {
            'fields': ('room_id', 'first_name', 'last_name', 'age')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_number')
        }),
    )

# Register the custom admin class with the FamilyMember model
admin.site.register(FamilyMember, FamilyMemberAdmin)

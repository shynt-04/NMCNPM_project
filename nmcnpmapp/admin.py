# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Payment, PaymentStatus, FamilyMember, Article
from django.db import IntegrityError
from .models import Article
from django.shortcuts import render
from django.contrib.auth.models import Group

admin.site.register(Article)

# CustomUserAdmin with both room_id uniqueness check and is_approved field handling
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('room_id', 'phone_number' ,'username', 'email', 'is_approved')  # Display room_id, email, and approval status
    list_filter = ('room_id', 'is_approved',)  # Filter by approval status
    search_fields = ('room_id', 'email')  # Allow searching by room_id and email

    # Customize the fields displayed on the add/edit page
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_approved',)}),  # Add 'is_approved' field to the form
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('room_id', 'is_approved')}),  # Add these fields to the add form as well
    )

    def save_model(self, request, obj, form, change):

        super().save_model(request, obj, form, change)  # Call the parent save_model method to actually save the object

# Register the CustomUser model with the admin
admin.site.register(CustomUser, CustomUserAdmin)

# Service view function (no changes needed here)
def service_view(request):
    user = request.user
    family_group = Group.objects.get(name='Tên group của bạn')  # Adjust group name as necessary
    is_member = family_group.user_set.filter(id=user.id).exists()

    return render(request, 'service.html', {'is_member': is_member})

# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Payment, PaymentStatus, FamilyMember, Article, RoomUser, SuperUser

# Register the Article model
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date')
    search_fields = ('title', 'author')
    list_filter = ('date',)
    readonly_fields = ('date',)

admin.site.register(Article, ArticleAdmin)

# Customized admin for RoomUser
@admin.register(RoomUser)
class RoomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'room_id', 'registry_email','phone_number','is_approved']
    search_fields = ['username', 'room_id', 'registry_email','phone_number','is_approved']

@admin.register(SuperUser)
class SuperUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','password']
    search_fields = ['username', 'email']

# Register other models
admin.site.register(Payment)
admin.site.register(PaymentStatus)
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

# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Payment, PaymentStatus, FamilyMember, Article, RoomUser

# Register the Article model
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date')
    search_fields = ('title', 'author')
    list_filter = ('date',)
    readonly_fields = ('date',)

admin.site.register(Article, ArticleAdmin)

# Customized admin for RoomUser
class RoomUserAdmin(UserAdmin):  # Inherit from UserAdmin for User-specific functionality
    model = RoomUser
    # Fields to display in the list view
    list_display = ('room_id', 'username', 'is_approved', 'registry_email', 'phone_number')
    # Fields to filter by in the right sidebar
    list_filter = ('is_approved',)
    # Fields that are searchable
    search_fields = ('room_id', 'username', 'phone_number')
    # Ordering for the list view
    ordering = ('room_id',)
    # Read-only fields (optional, for fields you don’t want users to edit directly)
    readonly_fields = ('room_id',)

    # Customize the layout of the add/edit form with fieldsets
    fieldsets = (
        (None, {
            'fields': ('room_id', 'username', 'is_approved', 'password')
        }),
        ('Contact Information', {
            'fields': ('registry_email', 'phone_number')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'user_permissions', 'groups')
        }),
    )

# Register RoomUser with the custom admin class
admin.site.register(RoomUser, RoomUserAdmin)

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

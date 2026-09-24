from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_approved_doctor', 'is_staff')
    list_filter = ('role', 'is_approved_doctor', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'is_approved_doctor')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')

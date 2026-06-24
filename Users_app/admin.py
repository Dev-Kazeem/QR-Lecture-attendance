from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'student_id', 'is_staff']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username', 'first_name', 'last_name', 'email', 'student_id', 'password1', 'password2'),
        }),
    )
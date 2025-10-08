from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import User
from .forms import UserCreationForm, UserChangeForm



class UserAdmin(BaseUserAdmin):
    """User model appearence in admin panel"""
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "username", "is_staff"]
    list_filter = ["is_staff"]
    fieldsets = [
        (None, {"fields": ["email", "username", "password"]}),
        ("Permissions", {"fields": ["is_staff", "is_active"]}),
        ("Other", {"fields": ["created_at", "timezone"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "username", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "username", "created_at"]
    ordering = ["email"]
    readonly_fields = ["created_at"]

admin.site.register(User, UserAdmin)

from django import forms
from django.contrib import admin
from django.utils import timezone
from .models import Task, Reminding
from .forms import TaskForm


class TaskAdmin(admin.ModelAdmin):
    """Admin panel for tasks""" 
    list_display = ['title', 'user', 'status', 'deadline', 'id']
    list_filter = ['status', 'user']

    fieldsets = [
        (None, {'fields': ['title', 'description', 'priority', 'user']}),
        ('Status', {'fields': ['status', 'deadline', 'reminder']}),
        (None, {'fields': ['local_deadline', 'created_at', 'updated_at']}),
    ]

    search_fields = ['title', 'user__username', 'status']
    ordering = ["title"]
    readonly_fields = ["created_at", "updated_at", 'local_deadline']

admin.site.register(Task, TaskAdmin)
admin.site.register(Reminding)
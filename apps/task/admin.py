from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'deadline', 'is_completed')
    list_filter = ('is_completed', 'deadline', 'user')
    search_fields = ('title', 'description')

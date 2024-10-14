from django.contrib import admin

from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ["title", "completed", "created_at", "completed_at"]
    list_filter = ["completed", "created_at", "completed_at"]

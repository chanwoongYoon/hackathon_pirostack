from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["role", "phone_number", "password", "permission"]

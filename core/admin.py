from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("first_name", "last_name", "username")
    list_filter = ("is_staff", "is_active", "is_superuser")
    exclude = ("password",)
    readonly_fields = ("date_joined", "last_login")

from django.contrib import admin

from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):

    model = CustomUser

    fieldsets = (
        *UserAdmin.fieldsets,
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    search_fields = ('first_name', 'last_name', 'email',)
    list_filter = ('is_staff',)

admin.site.register(CustomUser, CustomUserAdmin)

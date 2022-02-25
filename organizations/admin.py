from django.contrib import admin

from core.utils import randomstr
import re

from .models import *


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization_id', 'status']
    fields = ['name', 'status', 'organization_id', 'created_user', 'created_at', 'last_updated']
    readonly_fields = ['organization_id', 'created_user', 'created_at', 'last_updated']
    search_fields = ('name', 'organization_id')
    list_per_page = 50

    # Adds the public id and created user before saving
    def save_model(self, request, obj, form, change):
        if obj.organization_id == None or obj.organization_id == '':
            obj.organization_id = randomstr()
        if obj.created_user == None:
            obj.created_user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Organization, OrganizationAdmin)


class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'status']
    fields = ['user', 'organization', 'role', 'status', 'created_at', 'last_updated']
    readonly_fields = ['user', 'organization', 'created_at', 'last_updated']
    list_per_page = 50

admin.site.register(OrganizationUser, OrganizationUserAdmin)


class OrganizationSettingsAdmin(admin.ModelAdmin):
    list_display = ['organization']
    fields = ['organization', 'multiple_loans_per_customer', 'created_at', 'last_updated']
    readonly_fields = ['organization', 'created_at', 'last_updated']
    list_per_page = 50

admin.site.register(OrganizationSettings, OrganizationSettingsAdmin)

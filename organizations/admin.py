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
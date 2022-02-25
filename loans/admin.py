from django.contrib import admin

from core.utils import randomstr
import re

from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'status']
    fields = ['name', 'status', 'organization', 'created_user', 'created_at', 'last_updated']
    readonly_fields = ['organization', 'created_user', 'created_at', 'last_updated']
    search_fields = ('name',)
    list_per_page = 50

    def has_add_permission(self, request):
        return False

admin.site.register(Product, ProductAdmin)


class ProductConfigAdmin(admin.ModelAdmin):
    list_display = ['product', 'label', 'current']
    fields = ['product', 'label', 'current', 'created_user', 'created_at', 'last_updated']
    readonly_fields = ['product', 'created_user', 'created_at', 'last_updated']
    search_fields = ('label',)
    list_per_page = 50

    def has_add_permission(self, request):
        return False

admin.site.register(ProductConfig, ProductConfigAdmin)
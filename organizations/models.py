from django.db import models
from django.db.models import JSONField

from django.conf import settings

from customers.models import *


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    organization_id  = models.CharField(max_length=16, null=False, blank=True)

    ORGANIZATION_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )
    
    status = models.CharField(
        max_length=25,
        choices=ORGANIZATION_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.name


class OrganizationUser(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    ORGANIZATION_USER_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )

    status = models.CharField(
        max_length=25,
        choices=ORGANIZATION_USER_STATUS,
        blank=False,
        default='active',
    )

    ORGANIZATION_ROLE = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    role = models.CharField(
        max_length=25,
        choices=ORGANIZATION_ROLE,
        blank=False,
        default='user',
    )

    def __str__(self):
        return str(self.id)


class OrganizationCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    ORGANIZATION_CUSTOMER_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
    )

    status = models.CharField(
        max_length=25,
        choices=ORGANIZATION_CUSTOMER_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.id


class OrganizationSettings(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.SET_NULL, null=True)
    multiple_loans_per_customer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
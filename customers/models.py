from django.db import models
from django.db.models import JSONField

from django.conf import settings


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=32, null=False, blank=True)
    customer_number = models.CharField(max_length=16, null=False, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    CUSTOMER_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
    )
    
    status = models.CharField(
        max_length=25,
        choices=CUSTOMER_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return str(self.id)


class CustomerKYC(models.Model):
    id = models.AutoField(primary_key=True)
    customer_kyc_id = models.CharField(max_length=32, null=False, blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)

    first_name = models.CharField(max_length=200, null=False, blank=True)
    last_name = models.CharField(max_length=200, null=False, blank=True)
    birth_date = models.DateTimeField(null=False, blank=True)
    address = models.TextField(null=False, blank=True)
    phone_number = models.CharField(max_length=25, null=False, blank=True)
    national_id = models.CharField(max_length=50, null=False, blank=True)

    CUSTOMER_GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    status = models.CharField(
        max_length=25,  
        choices=CUSTOMER_GENDER,
        blank=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    CUSTOMER_KYC_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )
    
    status = models.CharField(
        max_length=25,
        choices=CUSTOMER_KYC_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return str(self.id)
    
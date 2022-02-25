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
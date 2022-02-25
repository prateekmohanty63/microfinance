from django.db import models
from django.db.models import JSONField

from django.conf import settings

from organizations.models import *
from customers.models import *


class OrganizationSettings(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.SET_NULL, null=True)
    allow_multiple_loans = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=16, null=False, blank=True)
    label = models.CharField(max_length=200, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    PRODUCT_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )
    
    status = models.CharField(
        max_length=25,
        choices=PRODUCT_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.label


class ProductConfig(models.Model):
    id = models.AutoField(primary_key=True)
    product_config_id = models.CharField(max_length=16, null=False, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    length = models.IntegerField(null=False, blank=False)
    overdue_on_day = models.IntegerField(null=False, blank=False)
    default_on_day = models.IntegerField(null=False, blank=False)
    payment_config = models.ForeignKey('PaymentConfig', on_delete=models.SET_NULL, null=True)
    interest_config = models.ForeignKey('InterestConfig', on_delete=models.SET_NULL, null=True)
    fee_config = models.ForeignKey('FeeConfig', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    PRODUCT_CONFIG_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )
    
    status = models.CharField(
        max_length=25,
        choices=PRODUCT_CONFIG_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.id


class InterestConfig(models.Model):
    id = models.AutoField(primary_key=True)
    interest_config_id = models.CharField(max_length=16, null=False, blank=True)
    label = models.CharField(max_length=200, null=True, blank=True)
    day = models.IntegerField(null=False, blank=False)
    amount = models.FloatField(null=True, blank=True)

    INTEREST_CONFIG_STRUCTURE = (
        ('principle-percentage', 'Percentage of Principal'),
        ('loan-percentage', 'Percentage of Loan Amount'),
        ('flat-fee', 'Flat Fee'),
    )
    
    config = models.CharField(
        max_length=25,
        choices=INTEREST_CONFIG_STRUCTURE,
        blank=False,
    )

    INTEREST_CONFIG_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )
    
    status = models.CharField(
        max_length=25,
        choices=INTEREST_CONFIG_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.id


class FeeConfig(models.Model):
    id = models.AutoField(primary_key=True)
    fee_config_id = models.CharField(max_length=16, null=False, blank=True)
    label = models.CharField(max_length=200, null=True, blank=True)
    day = models.IntegerField(null=False, blank=False)
    amount = models.FloatField(null=True, blank=True)

    FEE_CONFIG_STRUCTURE = (
        ('flat-fee', 'Flat Fee'),
        ('principle-percentage', 'Percentage of Principal'),
        ('loan-percentage', 'Percentage of Loan Amount'),
    )
    
    structure = models.CharField(
        max_length=25,
        choices=FEE_CONFIG_STRUCTURE,
        blank=False,
    )

    FEE_CONFIG_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )
    
    status = models.CharField(
        max_length=25,
        choices=FEE_CONFIG_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.id


class PaymentConfig(models.Model):
    id = models.AutoField(primary_key=True)
    payment_config_id = models.CharField(max_length=16, null=False, blank=True)
    label = models.CharField(max_length=200, null=True, blank=True)
    day = models.IntegerField(null=False, blank=False)
    amount = models.FloatField(null=True, blank=True)

    PAYMENT_CONFIG_STRUCTURE = (
        ('flat-amount', 'Flat Amount'),
        ('principle-percentage', 'Percentage of Principal'),
        ('loan-percentage', 'Percentage of Loan Amount'),
    )
    
    structure = models.CharField(
        max_length=25,
        choices=PAYMENT_CONFIG_STRUCTURE,
        blank=False,
    )

    PAYMENT_CONFIG_STATUS = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('deleted', 'Deleted'),
    )
    
    status = models.CharField(
        max_length=25,
        choices=PAYMENT_CONFIG_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.id
    

class Loan(models.Model):
    id = models.AutoField(primary_key=True)
    loan_id = models.CharField(max_length=32, null=False, blank=True)
    loan_number = models.CharField(max_length=16, null=False, blank=True)
    customer = product = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('ProductConfig', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    LOAN_STATUS = (
        ('active', 'Active'),
        ('void', 'Void'),
        ('cleared', 'Cleared'),
        ('overdue', 'Overdue'),
        ('default', 'Default'),
    )
    
    status = models.CharField(
        max_length=25,
        choices=LOAN_STATUS,
        blank=False,
        default='active',
    )

    def __str__(self):
        return self.id

    
class Interest(models.Model):
    id = models.AutoField(primary_key=True)
    interest_id = models.CharField(max_length=32, null=False, blank=True)
    amount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    payment_id = models.CharField(max_length=32, null=False, blank=True)
    payment_number = models.CharField(max_length=16, null=False, blank=True)
    amount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    
class Fee(models.Model):
    id = models.AutoField(primary_key=True)
    fee_id = models.CharField(max_length=32, null=False, blank=True)
    fee_number = models.CharField(max_length=16, null=False, blank=True)
    amount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=32, null=False, blank=True)
    transaction_number = models.CharField(max_length=16, null=False, blank=True)
    loan = models.ForeignKey('Loan', on_delete=models.SET_NULL, null=True)
    fee = models.ForeignKey('Fee', on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True)
    interest = models.ForeignKey('Interest', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    TRANSACTION_TYPE = (
        ('payment', 'Payment'),
        ('interest', 'Interest'),
        ('fee', 'Fee'),
    )
    
    type = models.CharField(
        max_length=25,
        choices=TRANSACTION_TYPE,
        blank=False,
        default='applied',
    )

    TRANSACTION_STATUS = (
        ('applied', 'Applied'),
        ('voided', 'Voided'),
    )
    
    status = models.CharField(
        max_length=25,
        choices=TRANSACTION_STATUS,
        blank=False,
        default='applied',
    )

    def __str__(self):
        return self.id

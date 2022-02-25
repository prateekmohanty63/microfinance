from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import *
from organizations.models import Organization, OrganizationSettings
from customers.models import Customer
from loans.models import Product as LoanProduct
from loans.models import ProductConfig as LoanProductConfig
from loans.models import PaymentConfig as LoanPaymentConfig
from loans.models import InterestConfig as LoanInterestConfig
from loans.models import FeeConfig as LoanFeeConfig

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'name', 'isAdmin']

    def get_id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']
    
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_id(self, obj):
        return obj.id


class OrganizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = ['organization_id', 'name']


class OrganizationSettingsSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField(read_only=True)
    organization_id = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = OrganizationSettings
        fields = ['organization', 'organization_id', 'multiple_loans_per_customer']
    
    def get_organization(self, obj):
        return obj.organization.name

    def get_organization_id(self, obj):
        return obj.organization.organization_id


class LoanProductSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField(read_only=True)
    organization_id = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = LoanProduct
        fields = ['product_id', 'name', 'organization', 'organization_id']
    
    def get_organization(self, obj):
        return obj.organization.name

    def get_organization_id(self, obj):
        return obj.organization.organization_id


class LoanProductConfigSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    product_id = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = LoanProductConfig
        fields = ['product', 'product_id', 'product_config_id', 'label', 'length', 'overdue_on_day', 'default_on_day', 'current']
    
    def get_product(self, obj):
        return obj.product.name

    def get_product_id(self, obj):
        return obj.product.product_id


class LoanPaymentConfigSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    product_id = serializers.SerializerMethodField(read_only=True)
    product_config_id = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = LoanPaymentConfig
        fields = ['product', 'product_id', 'product_config_id', 'payment_config_id', 'label', 'structure', 'day', 'amount']
    
    def get_product(self, obj):
        return obj.product_config.product.name

    def get_product_id(self, obj):
        return obj.product_config.product.product_id
    
    def get_product_config_id(self, obj):
        return obj.product_config.product_config_id


class LoanInterestConfigSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    product_id = serializers.SerializerMethodField(read_only=True)
    product_config_id = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = LoanInterestConfig
        fields = ['product', 'product_id', 'product_config_id', 'interest_config_id', 'label', 'structure', 'day', 'amount']
    
    def get_product(self, obj):
        return obj.product_config.product.name

    def get_product_id(self, obj):
        return obj.product_config.product.product_id
    
    def get_product_config_id(self, obj):
        return obj.product_config.product_config_id


class LoanFeeConfigSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    product_id = serializers.SerializerMethodField(read_only=True)
    product_config_id = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = LoanFeeConfig
        fields = ['product', 'product_id', 'product_config_id', 'fee_config_id', 'label', 'structure', 'day', 'amount']
    
    def get_product(self, obj):
        return obj.product_config.product.name

    def get_product_id(self, obj):
        return obj.product_config.product.product_id
    
    def get_product_config_id(self, obj):
        return obj.product_config.product_config_id


class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['customer_id', 'customer_number']
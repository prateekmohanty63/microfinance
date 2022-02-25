from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import *
from organizations.models import Organization, OrganizationSettings
from loans.models import Product as LoanProduct


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
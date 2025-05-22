from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vendor, Supplier

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class VendorRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = ['user', 'name', 'email', 'phone_number', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        vendor = Vendor.objects.create(user=user, **validated_data)
        return vendor


class SupplierRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Supplier
        fields = ['user', 'name', 'contact_person', 'phone_number', 'email', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        supplier = Supplier.objects.create(user=user, **validated_data)
        return supplier


class VendorDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class SupplierDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

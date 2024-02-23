from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field that is write-only

    class Meta:
        model = Customer
        fields = ['id','first_name', 'last_name', 'email', 'phone', 'password']  # Include the password field

    def create(self, validated_data):
        password = validated_data.pop('password')  # Remove the password from validated_data
        user = User.objects.create_user(
            username=validated_data['email'], 
            email=validated_data['email'],
            password=password  # Use the password to create the user
        )
        customer = Customer.objects.create(user=user, **validated_data)
        return customer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Make password optional for updates

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Remove the password from validated_data
        user = User.objects.create_user(
            username=validated_data['email'], 
            email=validated_data['email'],
            password=password  # Use the password to create the user
        )
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

    def update(self, instance, validated_data):
        # Update the User associated with the Customer
        user = instance.user
        user.email = validated_data.get('email', user.email)
        if 'password' in validated_data:
            password = validated_data.pop('password')
            user.password = make_password(password)
        user.save()

        # Update Customer instance
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()

        return instance
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .models import Review

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id', 'model']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'content_type', 'object_id', 'user', 'text']

    def validate_content_type_id(self, value):
        allowed_models = ['book']
        try:
            content_type = ContentType.objects.get_for_id(value)
            if content_type.model not in allowed_models:
                raise serializers.ValidationError("Content type is not allowed.")
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content type.")
        return value

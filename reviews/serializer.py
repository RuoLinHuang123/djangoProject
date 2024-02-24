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
    # Remove 'user' from fields to prevent it from being input directly
    class Meta:
        model = Review
        fields = ['id', 'content_type', 'object_id', 'text']  # 'user' field is removed

    def validate(self, data):
        content_type = data.get('content_type')
        object_id = data.get('object_id')
        allowed_models = ['book']
        try:
            ct = ContentType.objects.get_for_id(content_type.id)
            if ct.model not in allowed_models:
                raise serializers.ValidationError({"content_type": "Content type is not allowed."})
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({"content_type": "Invalid content type."})

        model_class = ct.model_class()
        if not model_class.objects.filter(id=object_id).exists():
            raise serializers.ValidationError({"object_id": "No object found for the given id and content type."})

        return data

    def save(self, **kwargs):
        user = self.context.get('request').user if 'request' in self.context else None
        
        if user and user.is_authenticated:
            self.validated_data['user'] = user
            return super().save(**kwargs)
        else:
            raise serializers.ValidationError({"user": "No authenticated user found. Cannot proceed with saving the review."})
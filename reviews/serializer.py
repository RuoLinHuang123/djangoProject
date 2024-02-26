from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField(read_only=True)  # Add this line

    class Meta:
        model = Review
        fields = ['id', 'content_type', 'object_id', 'text', 'user_id']  # Include 'user_id'
    
    def get_user_id(self, obj):
        # This method returns the ID of the user who created the review
        return obj.user.id if obj.user else None

    def validate(self, data):
        content_type = data.get('content_type')
        object_id = data.get('object_id')
        try:
            ct = ContentType.objects.get_for_id(content_type.id)
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
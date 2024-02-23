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

    def validate(self, data):
        # Extract content_type and object_id from the input data
        content_type = data.get('content_type')
        object_id = data.get('object_id')

        # Validate content_type as before
        allowed_models = ['book']
        try:
            ct = ContentType.objects.get_for_id(content_type.id)
            if ct.model not in allowed_models:
                raise serializers.ValidationError({"content_type": "Content type is not allowed."})
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({"content_type": "Invalid content type."})

        # Validate that the specified object_id exists for the given content_type
        model_class = ct.model_class()  # Get the model class for the content type
        if not model_class.objects.filter(id=object_id).exists():
            raise serializers.ValidationError({"object_id": "No object found for the given id and content type."})

        # Return the validated data if all checks pass
        return data

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Review
from .serializer import ReviewSerializer



class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """
        Returns reviews, optionally filtered by a `user_id` query parameter in the URL.
        """
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Review.objects.filter(user_id=user_id).select_related('content_type', 'user')
        return Review.objects.all().select_related('content_type', 'user')


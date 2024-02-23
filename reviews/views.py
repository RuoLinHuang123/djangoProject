from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Review
from .serializer import ReviewSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all().select_related('content_type', 'user')
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned reviews to a given user,
        by filtering against a `user_id` query parameter in the URL.
        """
        queryset = self.queryset
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset


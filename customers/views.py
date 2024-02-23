from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Customer
from .serializer import CustomerSerializer


class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.select_related('user').all()


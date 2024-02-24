from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Customer
from .serializer import CustomerSerializer

class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.select_related('user').all()

    @action(detail=False, methods=['get', 'put'])
    def me(self, request):
        try:
            customer = Customer.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            return Response({"error": "Customer not found or not authenticated."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serialized_customer = CustomerSerializer(customer)
            return Response(serialized_customer.data)
        elif request.method == 'PUT':
            serialized_customer = CustomerSerializer(customer, data=request.data, partial=True)
            if serialized_customer.is_valid():
                serialized_customer.save()
                return Response(serialized_customer.data)
            return Response(serialized_customer.errors, status=status.HTTP_400_BAD_REQUEST)

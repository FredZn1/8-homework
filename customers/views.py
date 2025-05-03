from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from customers.models import Customer
from orders.models import Order
from customers.serializers import CustomerSerializer
from orders.serializers import OrderSerializer



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        customer = self.get_object()
        orders = Order.objects.filter(customer=customer)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

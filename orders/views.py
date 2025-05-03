from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').select_related('customer')
    serializer_class = OrderSerializer

    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        order = self.get_object()

        if set(request.data.keys()) - {'status'}:
            return Response(
                {'detail': 'Faqat status maydonini yangilashga ruxsat berilgan.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

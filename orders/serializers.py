from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'products', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'status',
            'total_price',
            'shipping_address',
            'payment_method',
            'created_at',
            'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()


        for item_data in items_data:
            item_id = item_data.get('id', None)
            if item_id:
                item = OrderItem.objects.get(id=item_id, order=instance)
                item.quantity = item_data.get('quantity', item.quantity)
                item.price = item_data.get('price', item.price)
                item.save()
            else:
                OrderItem.objects.create(order=instance, **item_data)

        return instance

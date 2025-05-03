from rest_framework import serializers
from .models import Product, ProductImage
from categories.models import Category
from categories.serializers import CategorySerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'discount_price',
            'category',
            'stock',
            'is_active',
            'created_at',
            'updated_at',
            'images',
        ]

    def validate(self, data):
        if data.get('discount_price') and data['discount_price'] > data['price']:
            raise serializers.ValidationError("Chegirma narxi asl narxdan katta bo‘lmasligi kerak.")

        if data.get('stock') is not None and data['stock'] < 0:
            raise serializers.ValidationError("Stok miqdori manfiy bo‘lishi mumkin emas.")

        return data

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        images_data = validated_data.pop('images', [])

        category, _ = Category.objects.get_or_create(**category_data)

        product = Product.objects.create(category=category, **validated_data)

        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        return product

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        images_data = validated_data.pop('images', [])

        if category_data:
            category, _ = Category.objects.get_or_create(**category_data)
            instance.category = category

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for image_data in images_data:
            ProductImage.objects.update_or_create(product=instance, **image_data)

        return instance

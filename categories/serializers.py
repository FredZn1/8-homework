from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'parent',
            'children',
            'image',
            'created_at',
            'updated_at',
        ]

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Bu kategoriya nomi allaqachon mavjud.")
        return value

    def validate_parent(self, value):
        if value == self.instance:
            raise serializers.ValidationError("Kategoriya o‘zini o‘zi ota kategoriya qilib belgilay olmaydi.")
        return value

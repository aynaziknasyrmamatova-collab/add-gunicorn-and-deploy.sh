from rest_framework import serializers
from .models import Shop, Category, Product


class ShopSer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Shop
        fields = ('id', 'name', 'color', 'logo', 'user')
        read_only_fields = ('id', 'user')


ShopSerializer = ShopSer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.ReadOnlyField(source='shop.name')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = (
            'id',
            'shop',
            'category',
            'shop_name',
            'category_name',
            'title',
            'price',
            'stock',
            'image',
        )
        read_only_fields = ('id', 'shop_name', 'category_name')

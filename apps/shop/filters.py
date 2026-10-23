import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    price = django_filters.NumberFilter(field_name='price')

    category = django_filters.NumberFilter(field_name='category_id')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    shop = django_filters.NumberFilter(field_name='shop_id')
    shop_name = django_filters.CharFilter(field_name='shop__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['price', 'min_price', 'max_price', 'category', 'category_name', 'shop', 'shop_name']

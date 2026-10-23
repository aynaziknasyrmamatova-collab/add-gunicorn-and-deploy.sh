from django.contrib import admin
from .models import Shop, Category, Product


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'user')
    search_fields = ('name', 'color')
    list_filter = ('user',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'stock', 'shop', 'category')
    search_fields = ('title',)
    list_filter = ('shop', 'category')

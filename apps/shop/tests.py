from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.shop.models import Shop, Category, Product


class ShopAppTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='shopowner', password='password123')
        self.shop = Shop.objects.create(name='TechZone', color='silver', user=self.user)
        self.cat_laptops = Category.objects.create(name='Ноутбуки', description='Компьютеры')
        self.cat_phones = Category.objects.create(name='Смартфоны', description='Телефоны')

        self.p1 = Product.objects.create(
            title='MacBook Air M2',
            price=1200.00,
            stock=10,
            shop=self.shop,
            category=self.cat_laptops
        )
        self.p2 = Product.objects.create(
            title='Dell XPS 15',
            price=1800.00,
            stock=5,
            shop=self.shop,
            category=self.cat_laptops
        )
        self.p3 = Product.objects.create(
            title='iPhone 15 Pro',
            price=1100.00,
            stock=15,
            shop=self.shop,
            category=self.cat_phones
        )

    def test_products_list(self):
        response = self.client.get('/shop/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 3)

    def test_filter_by_category(self):
        response = self.client.get(f'/shop/products/?category={self.cat_laptops.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 2)
        for prod in results:
            self.assertEqual(prod['category'], self.cat_laptops.id)

    def test_filter_by_price(self):
        response = self.client.get('/shop/products/?min_price=1500&max_price=2000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Dell XPS 15')

    def test_filter_by_shop(self):
        response = self.client.get(f'/shop/products/?shop={self.shop.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 3)

    def test_create_category_and_product(self):
        self.client.force_authenticate(user=self.user)
        # Create category
        cat_res = self.client.post('/shop/categories/', {
            'name': 'Планшеты',
            'description': 'Планшетные ПК'
        }, format='json')
        self.assertEqual(cat_res.status_code, status.HTTP_201_CREATED)
        new_cat_id = cat_res.json()['id']

        # Create product
        prod_res = self.client.post('/shop/products/', {
            'shop': self.shop.id,
            'category': new_cat_id,
            'title': 'iPad Air',
            'price': '700.00',
            'stock': 20
        }, format='json')
        self.assertEqual(prod_res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(prod_res.json()['title'], 'iPad Air')

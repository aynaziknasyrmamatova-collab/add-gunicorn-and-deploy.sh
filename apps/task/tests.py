from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework import status
from apps.task.models import Task


class TaskAppTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.user = User.objects.create_user(username='taskuser', password='password123')
        self.now = timezone.now()

        self.t_future = Task.objects.create(
            title='Сдать ДЗ',
            deadline=self.now + timedelta(days=2, hours=2),
            user=self.user
        )
        self.t_past = Task.objects.create(
            title='Просроченная задача',
            deadline=self.now - timedelta(days=2),
            user=self.user
        )
        self.t_none = Task.objects.create(
            title='Без срока',
            deadline=None,
            user=self.user
        )

    def test_deadline_time_left_calculation(self):
        response = self.client.get('/task/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {t['title']: t['time_left'] for t in response.json()}

        self.assertEqual(data['Сдать ДЗ'], '2 days left')
        self.assertEqual(data['Просроченная задача'], 'Дедлайн просрочен')
        self.assertEqual(data['Без срока'], 'Дедлайн не указан')

    def test_grouped_endpoint(self):
        response = self.client.get('/task/grouped/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        grouped = response.json()

        expected_date = self.t_future.deadline.strftime('%Y-%m-%d')
        self.assertIn(expected_date, grouped)
        self.assertEqual(grouped[expected_date][0]['title'], 'Сдать ДЗ')
        self.assertIn('no_deadline', grouped)

    def test_group_by_query_param(self):
        response = self.client.get('/task/?group_by=date')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        grouped = response.json()
        expected_date = self.t_future.deadline.strftime('%Y-%m-%d')
        self.assertIn(expected_date, grouped)

    def test_cache_invalidation_on_create_and_update(self):
        # 1. Fill cache
        self.client.get('/task/')
        self.assertIsNotNone(cache.get('tasks'))

        # 2. Authenticate and create task -> cache should clear
        self.client.force_authenticate(user=self.user)
        res = self.client.post('/task/', {
            'title': 'Новая задача для проверки',
            'description': 'Тест кэша'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(cache.get('tasks'))

        # 3. Fill cache again
        self.client.get('/task/')
        self.assertIsNotNone(cache.get('tasks'))

        # 4. Update task -> cache should clear
        task_id = self.t_future.id
        update_res = self.client.patch(f'/task/{task_id}/', {
            'is_completed': True
        }, format='json')
        self.assertEqual(update_res.status_code, status.HTTP_200_OK)
        self.assertIsNone(cache.get('tasks'))

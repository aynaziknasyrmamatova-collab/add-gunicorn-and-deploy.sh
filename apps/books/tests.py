from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.books.models import Library, Books


class BooksAndLibraryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.library = Library.objects.create(
            name='Национальная библиотека',
            address='ул. Абдрахманова 208',
            city='Бишкек'
        )
        self.book1 = Books.objects.create(
            title='Манас',
            author='Саякбай Каралаев',
            price=1500.00,
            library=self.library
        )
        self.book2 = Books.objects.create(
            title='Первый учитель',
            author='Чынгыз Айтматов',
            price=600.00,
            library=self.library
        )

    def test_library_list_with_nested_books(self):
        response = self.client.get('/books/libraries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

        lib_data = data[0]
        self.assertEqual(lib_data['name'], 'Национальная библиотека')
        self.assertIn('books', lib_data)
        self.assertEqual(len(lib_data['books']), 2)
        titles = [b['title'] for b in lib_data['books']]
        self.assertIn('Манас', titles)
        self.assertIn('Первый учитель', titles)

    def test_cascade_delete_library(self):
        lib_id = self.library.id
        self.library.delete()
        self.assertFalse(Library.objects.filter(id=lib_id).exists())
        self.assertEqual(Books.objects.filter(library_id=lib_id).count(), 0)

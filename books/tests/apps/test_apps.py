from django.apps import apps
from django.test import TestCase
from books.apps import BooksConfig


class BooksConfigTest(TestCase):
    def test_books_config(self):
        self.assertEqual(BooksConfig.name, 'books')
        self.assertEqual(apps.get_app_config('books').name, 'books')
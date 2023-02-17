from django.test import TestCase
from books.models import Author


class AuthorTestCase(TestCase):

    def test_author_creation(self):
        author_name = "Philippe Lançon"
        author = Author.objects.create(name=author_name)
        self.assertEqual(author.name, author_name)
        self.assertEqual(str(author), author_name)
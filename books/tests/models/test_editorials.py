from django.test import TestCase
from books.models import Editorial


class EditorialTestCase(TestCase):

    def test_editorial_creation(self):
        editorial_name = "Anagrama"
        editorial = Editorial.objects.create(name=editorial_name)
        self.assertEqual(editorial.name, editorial_name)
        self.assertEqual(str(editorial), editorial_name)
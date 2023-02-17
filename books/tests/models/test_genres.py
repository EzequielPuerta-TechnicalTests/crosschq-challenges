from django.test import TestCase
from books.models import Genre


class GenreTestCase(TestCase):

    def test_genre_creation(self):
        genre_name = "No Ficción,Novedades"
        genre = Genre.objects.create(name=genre_name)
        self.assertEqual(genre.name, genre_name)
        self.assertEqual(str(genre), genre_name)
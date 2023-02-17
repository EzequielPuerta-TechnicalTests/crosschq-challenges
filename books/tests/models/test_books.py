from django.test import TestCase
from books.models import Book, Author, Reviewer, Genre, Editorial, Tag


class BookTestCase(TestCase):

    def setUp(self):
        self.title = "El colgajo"
        self.text = '\"Nada de lo que te dicen es, cuando entras en un mundo en el que lo que es no puede en verdad decirse\", afirma en El colgajo Philippe Lançon'
        self.slug = "el-colgajo"
        self.contacted = False
        self.external_links = "[\"<a target=\\\"_blank\\\" href= \\\"https://www.lanacion.com.ar/opinion/sobrevivir-a-la-masacre-de-charlie-hebdo-nid2345271\\\">Leer rese\\u00f1a completa</a>\"]"
        self.links = "[]"
        self.thumbnail = "https://desarrollomultimedias3.lanacion.com.ar/npradmin/media/libros_thumbnails/libros_tapas/978-84-339-8041-0_thumbnail.jpg"
        self.image = "https://desarrollomultimedias3.lanacion.com.ar/npradmin/media/libros_tapas/978-84-339-8041-0.jpg"
        self.author = Author.objects.create(name="Philippe Lançon")
        self.reviewer = Reviewer.objects.create(
            name="Felipe Fernández", 
            link="https://www.lanacion.com.ar/autor/felipe-fernandez-487")
        self.genre_names = ["No Ficción","Novedades"]
        self.genres = set(Genre.objects.create(name=genre_name)
                       for genre_name in self.genre_names)
        self.editorial = Editorial.objects.create(name="Anagrama")
        self.isbn = "978-84-339-8041-0"
        self.tag_names = ["no-ficcion", "novedades"]
        self.tags = set(Tag.objects.create(name=tag_name) for tag_name in self.tag_names)


    def test_book_creation(self):
        book = Book.objects.create(
            title=self.title,
            text=self.text,
            slug=self.slug,
            contacted=self.contacted,
            external_links=self.external_links,
            links=self.links,
            thumbnail=self.thumbnail,
            image=self.image,
            author=self.author,
            reviewer=self.reviewer,
            editorial=self.editorial,
            isbn=self.isbn)
        
        self.assertEqual(len(self.genres), len(self.genre_names))
        [self.assertIn(genre.name, self.genre_names) for genre in self.genres]
        book.genres.set(self.genres)
        self.assertEqual(len(self.tags), len(self.tag_names))
        [self.assertIn(tag.name, self.tag_names) for tag in self.tags]
        book.tags.set(self.tags)

        self.assertEqual(book.title, self.title)
        self.assertEqual(str(book), self.title)
        self.assertEqual(book.text, self.text)
        self.assertEqual(book.slug, self.slug)
        self.assertEqual(book.contacted, self.contacted)
        self.assertEqual(book.external_links, self.external_links)
        self.assertEqual(book.links, self.links)
        self.assertEqual(book.thumbnail, self.thumbnail)
        self.assertEqual(book.image, self.image)
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.reviewer, self.reviewer)
        self.assertSetEqual(set(book.genres.all()), self.genres)
        self.assertEqual(book.editorial, self.editorial)
        self.assertEqual(book.isbn, self.isbn)
        self.assertSetEqual(set(book.tags.all()), self.tags)
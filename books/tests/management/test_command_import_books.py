from django.test import TestCase
from books.management.commands.import_books import get_or_create_obj, get_tags, get_links, Command
from books.models import Book, Author, Reviewer, Genre, Editorial, Tag
import requests


class ImportBooksTestCase(TestCase):


    def setUp(self):
        self.endpoint = 'https://adminlibros.lanacion.com.ar/libros/2019/'


    def test_get_or_create_author(self):
        self.assertEqual(len(Author.objects.all()), 0)
        author = get_or_create_obj(Author, name="Philippe Lançon")
        self.assertEqual(len(Author.objects.all()), 1)
        self.assertIn(author, Author.objects.all())


    def test_get_or_create_genre(self):
        self.assertEqual(len(Genre.objects.all()), 0)
        genre = get_or_create_obj(Genre, name="No Ficción,Novedades")
        self.assertEqual(len(Genre.objects.all()), 1)
        self.assertIn(genre, Genre.objects.all())


    def test_get_or_create_tag(self):
        self.assertEqual(len(Tag.objects.all()), 0)
        tag = get_or_create_obj(Tag, name="no-ficcion")
        self.assertEqual(len(Tag.objects.all()), 1)
        self.assertIn(tag, Tag.objects.all())


    def test_get_or_create_editorial(self):
        self.assertEqual(len(Editorial.objects.all()), 0)
        editorial = get_or_create_obj(Editorial, name="Anagrama")
        self.assertEqual(len(Editorial.objects.all()), 1)
        self.assertIn(editorial, Editorial.objects.all())


    def test_get_or_create_reviewer(self):
        reviewer_name = "Felipe Fernández"
        link = "https://www.lanacion.com.ar/autor/felipe-fernandez-487"
        self.assertEqual(len(Reviewer.objects.all()), 0)
        reviewer = get_or_create_obj(Reviewer, name=reviewer_name, link=link)
        self.assertEqual(len(Reviewer.objects.all()), 1)
        self.assertIn(reviewer, Reviewer.objects.all())


    def test_get_or_create_book(self):
        _author = get_or_create_obj(Author, name="Philippe Lançon")
        _reviewer = get_or_create_obj(Reviewer, name="Felipe Fernández", link="https://www.lanacion.com.ar/autor/felipe-fernandez-487")
        _editorial = get_or_create_obj(Editorial, name="Anagrama")
        _external_links = get_links(["<a target=\\\"_blank\\\" href= \\\"https://www.lanacion.com.ar/2216234-recuperar-el-signo-politico-del-lenguaje\\\">Leer rese\\u00f1a completa</a>"])
        _links = get_links([])

        self.assertEqual(len(Book.objects.all()), 0)
        book = get_or_create_obj(Book,
            title="El colgajo",
            text='\"Nada de lo que te dicen es, cuando entras en un mundo en el que lo que es no puede en verdad decirse\", afirma en El colgajo Philippe Lançon',
            slug="el-colgajo",
            contacted=False,
            external_links=_external_links,
            links=_links,
            thumbnail="https://desarrollomultimedias3.lanacion.com.ar/npradmin/media/libros_thumbnails/libros_tapas/978-84-339-8041-0_thumbnail.jpg",
            image="https://desarrollomultimedias3.lanacion.com.ar/npradmin/media/libros_tapas/978-84-339-8041-0.jpg",
            author=_author,
            reviewer=_reviewer,
            editorial=_editorial,
            isbn="978-84-339-8041-0")
        genres = set(Genre.objects.create(name=genre_name) for genre_name in ["No Ficción","Novedades"])
        book.genres.set(genres)
        tags = set(Tag.objects.create(name=tag_name) for tag_name in ["no-ficcion", "novedades"])
        book.tags.set(tags)

        self.assertEqual(len(Book.objects.all()), 1)
        self.assertIn(book, Book.objects.all())


    def test_get_tags(self):
        self.assertEqual(len(Tag.objects.all()), 0)
        tags = get_tags(['ficcion', 'literatura-extranjera'])
        self.assertEqual(len(Tag.objects.all()), 2)
        (self.assertIn(tag, Tag.objects.all()) for tag in tags)


    def test_get_empty_tags(self):
        self.assertEqual(len(Tag.objects.all()), 0)
        for case in [None, {}, '', []]:
            self.assertEqual(get_tags(case), [])
            self.assertEqual(len(Tag.objects.all()), 0)


    def test_get_links(self):
        links = [
            "<a target=\\\"_blank\\\" href= \\\"https://www.lanacion.com.ar/opinion/sobrevivir-a-la-masacre-de-charlie-hebdo-nid2345271\\\">Leer rese\\u00f1a completa</a>", 
            "<a target=\\\"_blank\\\" href= \\\"https://www.lanacion.com.ar/2216234-recuperar-el-signo-politico-del-lenguaje\\\">Leer rese\\u00f1a completa</a>"]
        real_links = get_links(links)
        expected_links = [
            "https://www.lanacion.com.ar/opinion/sobrevivir-a-la-masacre-de-charlie-hebdo-nid2345271",
            "https://www.lanacion.com.ar/2216234-recuperar-el-signo-politico-del-lenguaje"]
        self.assertEqual(len(real_links), len(links))
        self.assertEqual(len(real_links), len(expected_links))
        (self.assertIn(expected_link, real_links) for expected_link in expected_links)


    def test_check_each_imported_book(self):
        (self.assertEqual(len(each.objects.all()), 0) 
            for each in (Book, Author, Reviewer, Genre, Editorial, Tag))

        result = requests.get(self.endpoint)
        Command().handle()
        if result.status_code == 200:
            for item in result.json():
                current_book = Book.objects.get(isbn=item.get('isbn'))
                self.assertEqual(current_book.title, item.get('title'))
                self.assertEqual(current_book.text, item.get('text'))
                self.assertEqual(current_book.slug, item.get('slug'))
                self.assertEqual(current_book.contacted, item.get('contacted', False))
                self.assertEqual(current_book.external_links, str(get_links(item.get('external_links', []))))
                self.assertEqual(current_book.links, str(get_links(item.get('links', []))))
                self.assertEqual(current_book.thumbnail, item.get('thumbnail', ''))
                self.assertEqual(current_book.image, item.get('image', ''))
                self.assertEqual(current_book.author.name, item.get('author'))
                self.assertEqual(current_book.reviewer.name, item.get('reviewer'))
                (self.assertTrue(each in current_book.reviewer.link) for each in item.get('reviewer_link').split('/'))
                self.assertSetEqual(set(genre.name for genre in current_book.genres.all()), set(item.get('genre').split(',')))
                self.assertEqual(current_book.editorial.name, item.get('editorial'))
                self.assertEqual(current_book.isbn, item.get('isbn'))
                self.assertSetEqual(set(tag.name for tag in current_book.tags.all()), set(item.get('tags')))

            (self.assertGreater(len(each.objects.all()), 0) 
                for each in (Book, Author, Reviewer, Genre, Editorial, Tag))


    def test_repeated_items_are_not_inserted(self):
        repeated_isbn = '978-84-17553-21-0'
        result = requests.get(self.endpoint)
        repeated_items = list(filter(lambda item: item.get('isbn') == repeated_isbn, result.json()))
        self.assertEqual(len(repeated_items), 2)
        self.assertEqual(repeated_items[0], repeated_items[1])

        self.assertEqual(len(Book.objects.all()), 0)
        Command().handle()
        self.assertEqual(len(Book.objects.filter(isbn=repeated_isbn)), 1)


    def test_different_books_with_identical_title_are_inserted(self):
        repeated_title = 'Cuentos Completos'
        result = requests.get(self.endpoint)
        identical_title = list(filter(lambda item: item.get('title') == repeated_title, result.json()))
        self.assertEqual(len(identical_title), 2)
        self.assertNotEqual(identical_title[0], identical_title[1])

        self.assertEqual(len(Book.objects.all()), 0)
        Command().handle()
        self.assertEqual(len(Book.objects.filter(title=repeated_title)), 2)
from serializer_test_case import SerializerTestCase
from books.models import Author, Book, Editorial, Genre, Reviewer, Tag
from books.serializers import AuthorSerializer, BookSerializer, EditorialSerializer, GenreSerializer, ReviewerSerializer, TagSerializer


class AuthorSerializerTestCase(SerializerTestCase):


    def test_author_serializer(self):
        author_name = "Philippe Lançon"
        author = Author.objects.create(name=author_name)
        serializer = AuthorSerializer(instance=author)
        self.expected_attributes.append('name')
        self.assertEqual(set(serializer.data.keys()), set(self.expected_attributes))
        self.assertEqual(serializer.data['name'], author_name)


class BookSerializerTestCase(SerializerTestCase):


    def test_book_serializer(self):
        title = "El colgajo"
        text = '\"Nada de lo que te dicen es, cuando entras en un mundo en el que lo que es no puede en verdad decirse\", afirma en El colgajo Philippe Lançon'
        slug = "el-colgajo"
        contacted = False
        external_links = "[\"<a target=\\\"_blank\\\" href= \\\"https://www.lanacion.com.ar/opinion/sobrevivir-a-la-masacre-de-charlie-hebdo-nid2345271\\\">Leer rese\\u00f1a completa</a>\"]"
        links = "[]"
        thumbnail = "https://desarrollomultimedias3.lanacion.com.ar/npradmin/media/libros_thumbnails/libros_tapas/978-84-339-8041-0_thumbnail.jpg"
        image = "https://desarrollomultimedias3.lanacion.com.ar/npradmin/media/libros_tapas/978-84-339-8041-0.jpg"
        author = Author.objects.create(name="Philippe Lançon")
        reviewer = Reviewer.objects.create(
            name="Felipe Fernández", 
            link="https://www.lanacion.com.ar/autor/felipe-fernandez-487")
        genre_names = ["No Ficción","Novedades"]
        genres = set(Genre.objects.create(name=genre_name) for genre_name in genre_names)
        editorial = Editorial.objects.create(name="Anagrama")
        isbn = "978-84-339-8041-0"
        tag_names = ["no-ficcion", "novedades"]
        tags = set(Tag.objects.create(name=tag_name) for tag_name in tag_names)

        book = Book.objects.create(
            title=title,
            text=text,
            slug=slug,
            contacted=contacted,
            external_links=external_links,
            links=links,
            thumbnail=thumbnail,
            image=image,
            author=author,
            reviewer=reviewer,
            editorial=editorial,
            isbn=isbn)
        book.genres.set(genres)
        book.tags.set(tags)
        
        serializer = BookSerializer(instance=book)
        self.expected_attributes.extend([
            'title',
            'text',
            'slug',
            'contacted',
            'external_links',
            'links',
            'thumbnail',
            'image',
            'author',
            'reviewer',
            'editorial',
            'isbn',
            'genres',
            'tags'])
        self.assertEqual(set(serializer.data.keys()), set(self.expected_attributes))
        self.assertEqual(serializer.data['title'], title)
        self.assertEqual(serializer.data['text'], text)
        self.assertEqual(serializer.data['slug'], slug)
        self.assertEqual(serializer.data['contacted'], contacted)
        self.assertEqual(serializer.data['external_links'], external_links)
        self.assertEqual(serializer.data['links'], links)
        self.assertEqual(serializer.data['thumbnail'], thumbnail)
        self.assertEqual(serializer.data['image'], image)
        self.assertEqual(serializer.data['author'], author.id)
        self.assertEqual(serializer.data['reviewer'], reviewer.id)
        self.assertEqual(serializer.data['editorial'], editorial.id)
        self.assertEqual(serializer.data['isbn'], isbn)
        self.assertEqual(serializer.data['genres'], [genre.id for genre in genres])
        self.assertEqual(serializer.data['tags'], [tag.id for tag in tags])


class EditorialSerializerTestCase(SerializerTestCase):


    def test_editorial_serializer(self):
        editorial_name = "Anagrama"
        editorial = Editorial.objects.create(name=editorial_name)
        serializer = EditorialSerializer(instance=editorial)
        self.expected_attributes.append('name')
        self.assertEqual(set(serializer.data.keys()), set(self.expected_attributes))
        self.assertEqual(serializer.data['name'], editorial_name)


class GenreSerializerTestCase(SerializerTestCase):


    def test_genre_serializer(self):
        genre_name = "No Ficción"
        genre = Genre.objects.create(name=genre_name)
        serializer = GenreSerializer(instance=genre)
        self.expected_attributes.append('name')
        self.assertEqual(set(serializer.data.keys()), set(self.expected_attributes))
        self.assertEqual(serializer.data['name'], genre_name)


class ReviewerSerializerTestCase(SerializerTestCase):


    def test_reviewer_serializer(self):
        reviewer_name = "Felipe Fernández"
        link = "https://www.lanacion.com.ar/autor/felipe-fernandez-487"
        reviewer = Reviewer.objects.create(name=reviewer_name, link=link)
        serializer = ReviewerSerializer(instance=reviewer)
        self.expected_attributes.extend(['name', 'link'])
        self.assertEqual(set(serializer.data.keys()), set(self.expected_attributes))
        self.assertEqual(serializer.data['name'], reviewer_name)
        self.assertEqual(serializer.data['link'], link)


class TagSerializerTestCase(SerializerTestCase):


    def test_tag_serializer(self):
        tag_name = "no-ficcion"
        tag = Tag.objects.create(name=tag_name)
        serializer = TagSerializer(instance=tag)
        self.expected_attributes.append('name')
        self.assertEqual(set(serializer.data.keys()), set(self.expected_attributes))
        self.assertEqual(serializer.data['name'], tag_name)

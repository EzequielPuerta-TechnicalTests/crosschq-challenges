from django.core.management.base import BaseCommand, CommandError
from books.models import Book, Author, Reviewer, Genre, Editorial, Tag
import requests


def get_links(links):
    start_string = "href="
    real_links = []
    for link in links:
        start_index = link.index(start_string)
        end_index = link.index(">", start_index)
        real_link = link[start_index+len(start_string):end_index].strip()
        real_links.append(real_link[1:len(real_link)-1])
    return real_links


def get_or_create_obj(klass, **kwargs):
    key = 'isbn' if klass is Book else 'name'
    query = klass.objects.filter(**{key:kwargs.get(key)})
    if len(query) == 0:
        return klass.objects.create(**kwargs)
    else:
        return query.first()


def get_tags(tags=None):
    if not tags or not isinstance(tags, list) or len(tags) == 0:
        return []
    return [get_or_create_obj(Tag, name=_t) for _t in tags]


class Command(BaseCommand):
    help = 'Imports the books from a dataset'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        res = requests.get('https://adminlibros.lanacion.com.ar/libros/2019/')
        if res.status_code != 200:
            raise CommandError('Cannot retrieve dataset, please try later!')
        data = res.json()
        for _item in data:
            _author = get_or_create_obj(Author, name=_item.get('author'))
            _reviewer = get_or_create_obj(Reviewer, name=_item.get('reviewer'), link=_item.get('reviewer_link'))
            _genres = [get_or_create_obj(Genre, name=genre_name) 
                      for genre_name in _item.get('genre').split(',')]
            _editorial = get_or_create_obj(Editorial, name=_item.get('editorial'))
            _external_links = get_links(_item.get('external_links', []))
            _links = get_links(_item.get('links', []))

            book = get_or_create_obj(Book,
                title=_item.get('title'),
                text=_item.get('text'),
                slug=_item.get('slug'),
                contacted=_item.get('contacted', False),
                external_links=_external_links,
                links=_links,
                thumbnail=_item.get('thumbnail', ''),
                image=_item.get('image', ''),
                author=_author,
                reviewer=_reviewer,
                editorial=_editorial,
                isbn=_item.get('isbn'))

            if len(book.genres.all()) == 0:
                for _genre in _genres:
                    book.genres.add(_genre)
            if len(book.tags.all()) == 0:
                for _tag in get_tags(_item.get('tags')):
                    book.tags.add(_tag)
            book.save()

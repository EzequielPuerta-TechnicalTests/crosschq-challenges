from django.contrib import admin
from books.models import Book
from django.db.models import Count


book_genres_amount = Book.objects.annotate(genres_count=Count('genres'))


class AmountOfGenresFilter(admin.SimpleListFilter):
    title = 'amount of genres'
    parameter_name = 'genres_amount'


    def lookups(self, request, model_admin):
        return (
            ('1', 'one'),
            ('2', 'two'),
            ('3', 'three'),
            ('+', 'more'))


    def queryset(self, request, queryset):
        if self.value() == '+':
            return book_genres_amount.filter(
                genres_count__gte=4)
        else:
            return book_genres_amount.filter(
                genres_count__exact=int(self.value()))


class BooksAdmin(admin.ModelAdmin):


    list_display = ['title', 'author', 'editorial', 'isbn', 'all_genres', 'all_tags']
    search_fields = ['title', 'genres__name', 'reviewer__name', 'author__name', 'editorial__name', 'tags__name', 'isbn']
    list_filter = ['genres', 'reviewer', AmountOfGenresFilter]


    def all_genres(self, book):
        return ', '.join(map(lambda genre: genre.name, book.genres.all()))
    all_genres.short_description = 'Genres'
    all_genres.admin_order_field = 'book__genres'


    def all_tags(self, book):
        return ', '.join(map(lambda tag: tag.name, book.tags.all()))
    all_tags.short_description = 'Tags'
    all_tags.admin_order_field = 'book__tags'


admin.site.register(Book, BooksAdmin)

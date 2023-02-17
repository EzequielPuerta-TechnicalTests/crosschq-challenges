"""Models for the Books app."""

from django.db import models


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Genre(BaseModel):
    name = models.CharField(max_length=100)


class Reviewer(BaseModel):
    name = models.CharField(max_length=200)
    link = models.URLField()


class Author(BaseModel):
    name = models.CharField(max_length=200)


class Editorial(BaseModel):
    name = models.CharField(max_length=100)


class Tag(BaseModel):
    name = models.CharField(max_length=50)


class Book(BaseModel):
    title = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, )
    links = models.TextField()
    external_links = models.TextField()
    contacted = models.BooleanField(default=False)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, )
    tags = models.ManyToManyField(Tag)
    text = models.TextField()
    isbn = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    image = models.URLField()
    thumbnail = models.URLField()

    def __str__(self):
        return self.title
from rest_framework import viewsets, permissions
from .serializers import *


# ViewSets define the view behavior. ---------------------------------------
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class EditorialViewSet(viewsets.ModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )


class ReviewerViewSet(viewsets.ModelViewSet):
    queryset = Reviewer.objects.all()
    serializer_class = ReviewerSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, )
from django.test import TestCase
from books.models import Tag


class TagTestCase(TestCase):

    def test_tag_creation(self):
        tag_name = "no-ficcion"
        tag = Tag.objects.create(name=tag_name)
        self.assertEqual(tag.name, tag_name)
        self.assertEqual(str(tag), tag_name)
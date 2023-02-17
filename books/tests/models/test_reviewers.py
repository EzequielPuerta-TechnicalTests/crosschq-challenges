from django.test import TestCase
from books.models import Reviewer


class ReviewerTestCase(TestCase):

    def test_reviewer_creation(self):
        reviewer_name = "Felipe Fernández"
        link = "https://www.lanacion.com.ar/autor/felipe-fernandez-487"
        reviewer = Reviewer.objects.create(name=reviewer_name, link=link)
        self.assertEqual(reviewer.name, reviewer_name)
        self.assertEqual(str(reviewer), reviewer_name)
        self.assertEqual(reviewer.link, link)
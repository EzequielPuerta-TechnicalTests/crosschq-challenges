from django.test import TestCase


class SerializerTestCase(TestCase):


    def setUp(self):
        self.expected_attributes = ['created_on', 'id']
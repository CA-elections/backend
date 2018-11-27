from django.test import TestCase
from api.models import Election, Notification, Vote
from .utils import send_emails

# Create your tests here.


class EmailTestCase(TestCase):
    def setUp(self):
        pass

    def test_send_message(self):
        pass

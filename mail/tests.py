# noinspection PyPackageRequirements
from django.test import TestCase
from django.core.mail import outbox
from api.models import Candidate, Election, Notification, Vote
from .utils import send_emails
import datetime

# Create your tests here.


class EmailTestCase(TestCase):
    def setUp(self):
        Candidate.objects.create(name="John", surname="Smith", annotation="Example", is_student=True)
        self.e1 = Election.objects.create(name="Student election 1", date_start=datetime.datetime.now() - datetime.timedelta(1),
                                     date_end=datetime.datetime.now() + datetime.timedelta(1), is_student=True)
        n1 = Notification.objects.create(code="ahoj", election=e1)
        Vote.objects.create(notification=n1, id_student=1)

    def test_send_student_election(self):
        send_emails(self.e1)

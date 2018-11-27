# noinspection PyPackageRequirements
from django.test import TestCase
import django.core.mail
from api.models import Candidate, Election, Notification, Vote
from .utils import send_emails_with_code
from django.conf import settings
import datetime
import bakalari_reader

# Create your tests here.


class EmailTestCase(TestCase):
    def setUp(self):
        Candidate.objects.create(name="John", surname="Smith", annotation="Example", is_student=True)
        self.e1 = Election.objects.create(name="Student election 1", date_start=datetime.datetime.now() - datetime.timedelta(1),
                                     date_end=datetime.datetime.now() + datetime.timedelta(1), is_student=True)
        self.n1 = Notification.objects.create(code="ahoj", election=self.e1)
        Vote.objects.create(notification=self.n1, id_student=1)

    def test_send_student_election(self):
        send_emails_with_code(self.e1)
        self.assertEqual(django.core.mail.outbox[-1].subject, settings.EMAIL_SUBJECT)
        self.assertEqual(django.core.mail.outbox[-1].body, self.n1.code)
        self.assertEqual(django.core.mail.outbox[-1].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(django.core.mail.outbox[-1].to[0], bakalari_reader.get_student_email(1))

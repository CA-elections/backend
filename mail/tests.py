# noinspection PyPackageRequirements
from django.test import TestCase
import django.core.mail
from api.models import Candidate, Election, Notification, Vote
from .utils import send_emails_with_code
from django.conf import settings
import datetime
import bakalari_reader


class EmailTestCase(TestCase):
    def setUp(self):
        self.student1 = 1
        Candidate.objects.create(name="John", surname="Smith", annotation="Example 1", is_student=True)
        self.e1 = Election.objects.create(name="Student election 1",
                                          date_start=datetime.datetime.now() - datetime.timedelta(1),
                                          date_end=datetime.datetime.now() + datetime.timedelta(1), is_student=True)
        self.n1 = Notification.objects.create(code="ahoj", election=self.e1)
        Vote.objects.create(notification=self.n1, id_student=self.student1)

        self.student2 = 12
        Candidate.objects.create(name="Jack", surname="Smith", annotation="Example 2", is_student=False)
        self.e2 = Election.objects.create(name="Parent election 1",
                                          date_start=datetime.datetime.now() - datetime.timedelta(1),
                                          date_end=datetime.datetime.now() + datetime.timedelta(1), is_student=False)
        self.n2 = Notification.objects.create(code="mahoj", election=self.e2)
        Vote.objects.create(notification=self.n2, id_student=self.student2)

    def test_send_student_election(self):
        self.assertEqual(self.n1.sent, False)
        send_emails_with_code(self.e1)
        self.assertEqual(self.n1.sent, True)
        self.assertEqual(django.core.mail.outbox[-1].subject, settings.EMAIL_SUBJECT)
        self.assertEqual(django.core.mail.outbox[-1].body, self.n1.code)
        self.assertEqual(django.core.mail.outbox[-1].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(django.core.mail.outbox[-1].to[0], bakalari_reader.get_student_email(self.student1))

    def test_send_parent_election(self):
        self.assertEqual(self.n2.sent, False)
        send_emails_with_code(self.e2)
        self.assertEqual(self.n2.sent, True)
        self.assertEqual(django.core.mail.outbox[-1].subject, settings.EMAIL_SUBJECT)
        self.assertEqual(django.core.mail.outbox[-1].body, self.n2.code)
        self.assertEqual(django.core.mail.outbox[-1].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(django.core.mail.outbox[-1].to[0], bakalari_reader.get_parent_email(self.student2))

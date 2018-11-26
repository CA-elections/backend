from django.test import TestCase
from django.core.mail import send_mail

# Create your tests here.


class SimpleEmailTestCase(TestCase):
    def test_send_message(self):
        send_mail("Test", "Email sending test", "volbytest@seznamq.cz", ["xsicp01@gjk.cz", "volbytest@seznam.cz"])

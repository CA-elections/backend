from django.core.mail import send_mail
from api.models import Notification
import datetime


def send_emails():
    now = datetime.datetime.now()
    for n in Notification.objects.filter(sent=False,
                                         election__date_end__gt=now,
                                         election__date_start_lt=now):
        pass

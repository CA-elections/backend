from django.core.mail import EmailMessage
from api.models import Notification
import datetime


def get_parent_email(student_id):
    pass


def send_emails():
    now = datetime.datetime.now()
    for n in Notification.objects.filter(sent=False,
                                         election__date_end__gt=now,
                                         election__date_start_lt=now):
        for v in n.votes:
            EmailMessage("Studentské volby", n.code, to=get_parent_email(v.student_id)).send()
            n.sent = True
            n.save()

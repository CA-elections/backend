from django.core.mail import EmailMessage
from api.models import Notification
from django.conf import settings
import datetime
import bakalari_reader


def send_emails_with_code():
    now = datetime.datetime.now()
    for n in Notification.objects.filter(sent=False,
                                         election__date_end__gt=now,
                                         election__date_start_lt=now):
        for v in n.votes:
            if n.election.is_student:
                msg = EmailMessage(settings.EMAIL_SUBJECT, n.code, to=bakalari_reader.get_student_email(v.student_id))
            else:
                msg = EmailMessage(settings.EMAIL_SUBJECT, n.code, to=bakalari_reader.get_parent_email(v.student_id))
            msg.send()
            n.sent = True
            n.save()


def send_emails_with_results():
    raise NotImplementedError

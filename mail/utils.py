from django.core.mail import EmailMessage
from api.models import Notification
from django.conf import settings
import datetime
import bakalari_reader


def send_emails_with_code(election=None):
    now = datetime.datetime.now()
    if election is None:
        notifications = Notification.objects.filter(sent=False,
                                                    election__date_end__gt=now,
                                                    election__date_start__lt=now)
    else:
        notifications = Notification.objects.filter(sent=False,
                                                    election__date_end__gt=now,
                                                    election__date_start__lt=now,
                                                    election=election)
    for n in notifications:
        for v in n.votes.all():
            if n.election.is_student:
                msg = EmailMessage(settings.EMAIL_SUBJECT, n.code, to=[bakalari_reader.get_student_email(v.id_student)])
            else:
                msg = EmailMessage(settings.EMAIL_SUBJECT, n.code, to=[bakalari_reader.get_parent_email(v.id_student)])
            msg.send()
            n.sent = True
            n.save()


def send_emails_with_results(election=None):
    raise NotImplementedError

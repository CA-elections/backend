from django.core.mail import EmailMessage
from api.models import Notification
from django.conf import settings
import datetime
import bakalari_reader
from pytz import timezone

tz = timezone(settings.TIME_ZONE)


def send_emails_with_code(election=None):
    now = datetime.datetime.now(tz)
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
        codes = "";
        for v in n.votes.all():
            codes += n.code;
        if n.election.is_student:
            msg = EmailMessage(settings.EMAIL_SUBJECT, settings.EMAIL_TEMPLATE.format(codes=codes),
                               to=[bakalari_reader.get_student_email(v.id_student)])
        else:
            msg = EmailMessage(settings.EMAIL_SUBJECT, n.code, to=[bakalari_reader.get_parent_email(v.id_student)])
        msg.send()
        n.sent = True
        n.save()


def send_emails_with_results(election=None):
    raise NotImplementedError

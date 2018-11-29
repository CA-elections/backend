from django.core.mail import EmailMessage
from smtplib import SMTPException
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
        if not n.votes.count():
            continue
        v = n.votes.first()
        if n.election.is_student:
            msg = EmailMessage(settings.EMAIL_SUBJECT, settings.EMAIL_TEMPLATE.format(code=n.code),
                               to=[bakalari_reader.get_student_email(v.id_student)])
        else:
            msg = EmailMessage(settings.EMAIL_SUBJECT, settings.EMAIL_TEMPLATE.format(code=n.code), to=[bakalari_reader.get_parent_email(v.id_student)])
        try:
            msg.send()
        except SMTPException:
            pass
        else:
            n.sent = True
            n.save()


def send_emails_with_results(election=None):
    now = datetime.datetime.now(tz)
    if election is None:
        notifications = Notification.objects.filter(election__are_results_sent=False,
                                                    election__date_end__lt=now)
    else:
        notifications = Notification.objects.filter(election__are_results_sent=False,
                                                    election__date_end__lt=now,
                                                    election=election)
    current_election = None
    election_changed = True
    results_not_send = False
    for n in notifications:
        if current_election != n.election.pk:
            current_election = n.election.pk
            election_changed = True
            if not n.election.are_results_sent:
                results_not_send = True
        if not n.votes.count():
            continue
        v = n.votes.first()
        if n.election.is_student:
            msg = EmailMessage(settings.EMAIL_RESULTS_SUBJECT, settings.EMAIL_RESULTS_TEMPLATE,
                               to=[bakalari_reader.get_student_email(v.id_student)])
        else:
            msg = EmailMessage(settings.EMAIL_RESULTS_SUBJECT, settings.EMAIL_RESULTS_TEMPLATE,
                               to=[bakalari_reader.get_parent_email(v.id_student)])
        if results_not_send:
            msg.send(fail_silently=True)
        if election_changed and results_not_send:
            n.election.are_results_sent = True
            n.election.save()




from django.core.mail import EmailMessage
from smtplib import SMTPException
from api.models import Notification
from api.models import Score
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
            msg = EmailMessage(settings.EMAIL_SUBJECT.format(name=n.election.name), settings.EMAIL_TEMPLATE.format(code=n.code, description=n.election.description, name=n.election.name),
                               to=[bakalari_reader.get_student_email(v.id_student)])
        else:
            msg = EmailMessage(settings.EMAIL_SUBJECT.format(name=n.election.name), settings.EMAIL_TEMPLATE.format(code=n.code, description=n.election.description, name=n.election.name), to=[bakalari_reader.get_parent_email(v.id_student)])
        msg.content_subtype = "html"
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
        data = Score.objects.filter(election__pk=n.election.pk).order_by('-votes')
        if len(data) > 1 and data[0].votes == data[1].votes:
            election_results = "Volby skončily remízou."
        elif len(data) > 0:
            election_results = "Volby vyhrál kandidát " + data.first().candidate.name+" "+data.first().candidate.surname+"."
        else:
            election_results = "Voleb se nezúčastnil žádný kadidát."
        if n.election.is_student:
            msg = EmailMessage(settings.EMAIL_RESULTS_SUBJECT.format(name=n.election.name), settings.EMAIL_RESULTS_TEMPLATE.format(candidate=election_results),
                               to=[bakalari_reader.get_student_email(v.id_student)])
        else:
            msg = EmailMessage(settings.EMAIL_RESULTS_SUBJECT.format(name=n.election.name), settings.EMAIL_RESULTS_TEMPLATE.format(candidate=election_results),
                               to=[bakalari_reader.get_parent_email(v.id_student)])
        if results_not_send:
            msg.send(fail_silently=True)
        if election_changed and results_not_send:
            n.election.are_results_sent = True
            n.election.save()




from django.conf import settings
from .models import Election, Notification, Vote
import datetime
import bakalari_reader
from logger import log
from pytz import timezone
from mail.utils import send_emails_with_code, send_emails_with_results

tz = timezone(settings.TIME_ZONE)


def generate_notifications():
    now = datetime.datetime.now(tz)
    for election in Election.objects.filter(are_notifs_generated=False, date_start__lte=now, date_end__gt=now):
        log("generating notifications (and votes) for an election (name: " + election.name + ")")
        log("election started at " + str(election.date_start))
        if not election.is_student:
            notifs = bakalari_reader.get_all_youth_by_parent()
            for notif in notifs:
                new_notification = Notification(election=election, sent=False, used=False)
                new_notification.save()
                for idstud in notif:
                    new_vote = Vote(notification=new_notification, id_student=idstud)
                    new_vote.save()
        else:
            notifs = bakalari_reader.get_all_oldenough()
            for idstud in notifs:
                new_notification = Notification(election=election, sent=False, used=False)
                new_notification.save()
                new_vote = Vote(notification=new_notification, id_student=idstud)
                new_vote.save()
        election.are_notifs_generated = True
        election.save()


def runtasks():
    log("RUNNING ROUTINE AUTOMATED TASKS at " + str(datetime.datetime.now(tz)))
    log("checking for running elections without notifications generated")
    generate_notifications()
    log("sending unsent voting notifications")
    send_emails_with_code()
    log("sending unsent results emails")
    send_emails_with_results()
    print("ROUTINE AUTOMATED TASKS FINISHED")

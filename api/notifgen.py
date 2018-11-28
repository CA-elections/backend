from .models import Election, Notification, Vote
import datetime
import bakalari_reader
from generators import generatevotecode


def generate_notifications():
    now = datetime.datetime.now()
    for election in Election.objects.filter(are_notifs_generated=False, date_start_gte=now):
        if not election.is_student:
            notifs = bakalari_reader.get_all_youth_by_parent()
            for notif in notifs:
                new_notification = Notification(election=election, sent=False, code=generatevotecode(), used=False)
                new_notification.save()
                for idstud in notif:
                    new_vote = Vote(notification=new_notification, id_student=idstud)
                    new_vote.save()
        else:
            notifs = bakalari_reader.get_all_oldenough()
            for idstud in notifs:
                new_notification = Notification(election=election, sent=False, code=generatevotecode(), used=False)
                new_notification.save()
                new_vote = Vote(notification=new_notification, id_student=idstud)
                new_vote.save()
        election.are_notifs_generated = True
        election.save()


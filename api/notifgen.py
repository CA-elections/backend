from .models import Election, Notification, Vote
import datetime
import bakalari_reader


def generate_notifications():
    now = datetime.datetime.now()
    for election in Election.objects.filter(are_notifs_generated=False, date_start__lte=now, date_end__gte=now):
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


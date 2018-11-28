from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    is_student = models.BooleanField(default=False)


class Election(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    is_student = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    description = models.TextField(default="")
    are_notifs_generated = models.BooleanField(default=False)


class Notification(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='notifications')

    sent = models.BooleanField(default=False)
    code = models.CharField(max_length=100)
    used = models.BooleanField(default=False)


class Vote(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='votes')

    id_student = models.IntegerField()


class Score(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='elections')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')

    votes = models.IntegerField(default=0)
    annotation = models.TextField(default="")

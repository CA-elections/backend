from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    annotation = models.CharField(max_length=3000)
    is_student = models.BooleanField()


class Election(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    is_student = models.BooleanField()
    name = models.CharField(max_length=200)


class Notification(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='notifiactions')

    sent = models.BooleanField()
    code = models.CharField(max_length=100)
    used = models.BooleanField()


class Vote(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='votes')

    id_student = models.IntegerField()


class Score(models.Model):
    candidate = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='scores')
    election = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='vote_counts')

    votes = models.IntegerField()

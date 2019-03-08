from django.contrib import admin
from .models import Candidate, Election, Notification, Vote, Score
# Register your models here.

admin.site.register(Candidate)
admin.site.register(Election)
admin.site.register(Notification)
admin.site.register(Vote)
admin.site.register(Score)

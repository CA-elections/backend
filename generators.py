#!/usr/bin/env python
import os
import sys
import time
import random
import datetime

from datetime import date
from pytz import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django

django.setup()

from django.conf import settings

tz = timezone(settings.TIME_ZONE)

from api.models import Candidate, Election, Score, Notification, Vote
import bakalari_reader
from logger import log

# generates a random date a few days before or after today
def datearoundnow():
    return tz.localize(datetime.datetime(2018, 11, 30)) + datetime.timedelta(days=random.randint(-20, 30))

# generates a random date a few days after the date given
def enddate(startdate):
    return startdate + datetime.timedelta(days=random.randint(2, 7))

# chooses a random vowel or a combination of vowels
def genvowel():
    vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'oe', 'ue', 'ae', 'ou']
    return vowels[random.randint(0, len(vowels) - 1)]

# chooses a random consonant
def genconsonant():
    proh = ['a', 'e', 'i', 'o', 'u', 'y']
    while True:
        num = ord('a') + random.randint(0, 25)
        fail = False
        for lett in proh:
            if (ord(lett) == num):
                fail = True
        if (not fail):
            return str(chr(num))

# generates a word by combining random letters
def genword():
    outstr = ""
    for i in range(3):
        outstr += genconsonant()
        outstr += genvowel()
    return outstr

# chooses a random verb
def genverb():
    verbs = ['see', 'take', 'welcome', 'amuse', 'turn', 'flip', 'narrow', 'expand', 'walk with', 'talk to', 'do not be scared by', 'await', 'search for']
    return verbs[random.randint(0, len(verbs) - 1)]

# chooses a random noun
def gennoun():
    nouns = ['the hill', 'the Sun', 'the Earth', 'the numbers', 'the flowers', 'me', 'everyone', 'a cup', 'any thought', 'the rest of the cake', 'aliens', 'philosophy', 'fun', 'power', 'an end']
    return nouns[random.randint(0, len(nouns) - 1)]

# returns the given word with the first letter capitalized
def capfirst(word):
    return word[0].capitalize() + word[1:]

# generates and adds to the database a random election. Simulates votes at random if the election has already started
# uses the Candidate database to choose candidates from there
def addnewelection(start, end):
    stud = (random.randint(0, 1) == 0)
    elename = "The " + capfirst(genword()) + " Election"
    desc = "Please " + genverb() + " " + gennoun() + ". Thank you."
    new_ele = Election(date_start=start, date_end=end, is_student=stud, name=elename, description=desc, are_notifs_generated=True)
    new_ele.save()
    c1, c2, c3 = Candidate.objects.filter(is_student=stud).order_by('?').all()[:3]
    vot1 = vot2 = vot3 = 0
    now = datetime.datetime.now(tz)

    # notification are not yet generated for the election
    if (now < start or (now < end and random.randint(0, 2) == 0)):
        new_ele.are_notifs_generated = False
        new_ele.save()
    # notification are alrady generated, some votes are casted
    else:
        vot1 = vot2 = vot3 = 0
        if (not stud):
            notifs = bakalari_reader.get_all_youth_by_parent()
            for notif in notifs:
                issent = not (random.randint(0, 6) == 0)
                isused = False
                if issent:
                    isused = (random.randint(0, 1) == 0)
                    if isused:
                        for i in notif:
                            val = random.randint(0, 3)
                            if val == 0:
                                vot1 += 1
                            elif val == 1:
                                vot2 += 1
                            elif val == 2:
                                vot3 += 1
                new_notification = Notification(election=new_ele, sent=issent, used=isused)
                new_notification.save()
                for idstud in notif:
                    new_vote = Vote(notification=new_notification, id_student=idstud)
                    new_vote.save()
        else:
            notifs = bakalari_reader.get_all_oldenough()
            for idstud in notifs:
                issent = not (random.randint(0, 7) == 0)
                isused = False
                if issent:
                    isused = (random.randint(0, 1) == 0)
                    if isused:
                        val = random.randint(0, 3)
                        if val == 0:
                            vot1 += 1
                        elif val == 1:
                            vot2 += 1
                        elif val == 2:
                            vot3 += 1
                new_notification = Notification(election=new_ele, sent=issent, used=isused)
                new_notification.save()
                new_vote = Vote(notification=new_notification, id_student=idstud)
                new_vote.save()
    
    new_score1 = Score(election=new_ele, candidate=c1, votes=vot1)
    new_score2 = Score(election=new_ele, candidate=c2, votes=vot2)
    new_score3 = Score(election=new_ele, candidate=c3, votes=vot3)
    new_score1.save()
    new_score2.save()
    new_score3.save()

# generate a annotation for a candidate and an election
def generateannotation():
    return "This candidate is " + genquality() + " and they live in " + capfirst(genword()) + "."
            
# generates a random sequence of characters which is to be used as a voting code
def generatevotecode():
    code = ''
    for i in range(16):
        code += str(chr(ord('a') + random.randint(0, 25)))
    return code + "!!EXPERIMENTAL!!"
    
# randomly chooses a personal first name
def genfirstname():
    names = ["Mike", "Elis", "Ellinor", "Ralph", "Eduard", "Emil", "Frederick", "Frederic", "Frederik", "Leopold", "Maria", "Anthony", "Anna", "Valeria", "Alexandra"]
    return names[random.randint(0, len(names) - 1)]

# randomly chooses an adjective (or equivalent) for auto-generated candidate annotations
def genquality():
    qualities = ["good", "very smelly", "excellent", "meh", "bad", "terrible", "fine", "awesome", "nice to old men", "funny"]
    return qualities[random.randint(0, len(qualities) - 1)]

# generates and adds to the database a new random candidate
def addcandidate(stud):
    firstname = capfirst(genword()) + " " + genfirstname()
    lastname = capfirst(genword())
    annotation=generateannotation()
    new_cand = Candidate(name=firstname, surname=lastname, is_student=stud, annotation=annotation)
    new_cand.save()

# database override
log("deleting all candidates")
Candidate.objects.all().delete()

log("creating new random candidates")
for i in range(12):
    addcandidate(random.randint(0, 1) == 0)

log("creating student and non-student candidates")
for i in range(3):
    addcandidate(True)
    addcandidate(False)

log("deleting all elections, votes, notifications")
Election.objects.all().delete()
Vote.objects.all().delete()
Notification.objects.all().delete()

log("creating new elections: the already started ones also with votes and notifications")
for i in range(7):
    start = datearoundnow()
    addnewelection(start, enddate(start))

for i in range(4):
    start = datetime.datetime.now(tz) + datetime.timedelta(days=random.randint(-3, -1))
    end = datetime.datetime.now(tz) + datetime.timedelta(days=random.randint(2, 5))
    addnewelection(start, end)

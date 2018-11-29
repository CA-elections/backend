#!/usr/bin/env python

"""
Executable python file. Clears databases with elections, candidates, votes, notifications and populates them with new randomly generated data.
"""

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

"""
Generates a random datetime a few days before or after now.
"""
def datearoundnow():
    days = random.randint(-20, 30)

    if days == 0:
        days = 1

    return datetime.datetime.now(tz) + datetime.timedelta(days)

"""
Generates a random datetime a few days after the datetime given.
"""
def enddate(startdate):
    return startdate + datetime.timedelta(days=random.randint(2, 7))

"""
Chooses a random vowel (consits of one or two characters).
"""
def genvowel():
    vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'oe', 'ue', 'ae', 'ou']
    return vowels[random.randint(0, len(vowels) - 1)]

"""
Chooses a random consonant.
"""
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

"""
Generates a word, few characters long and with no meaning, which is pronouncable due to an adequate combination of consonants and vowels.
"""
def genword():
    outstr = ""
    for i in range(3):
        outstr += genconsonant()
        outstr += genvowel()
    return outstr

"""
Chooses a random verb from a predefined list. Can include multiple words, such as prepositions.
"""
def genverb():
    verbs = ['see', 'take', 'welcome', 'amuse', 'turn', 'flip', 'narrow', 'expand', 'walk with', 'talk to', 'do not be scared by', 'await', 'search for']
    return verbs[random.randint(0, len(verbs) - 1)]

"""
Chooses a random subject from a predefined list to be used in a sentence. Can include multiple words, typically includes a noun.
"""
def gennoun():
    nouns = ['the hill', 'the Sun', 'the Earth', 'the numbers', 'the flowers', 'me', 'everyone', 'a cup', 'any thought', 'the rest of the cake', 'aliens', 'philosophy', 'fun', 'power', 'an end']
    return nouns[random.randint(0, len(nouns) - 1)]

"""
Returns the given string with the first character capitalized.
"""
def capfirst(word):
    return word[0].capitalize() + word[1:]

"""
Randomly generates a new election and adds it to the database.
That also might include Vote and Notification objects being added to the respective databases. These modifications also use elements of randomness.
The created elections use candidates already present in the Candidate database.
"""
def addnewelection(start, end):
    # whether the election should be a student election
    stud = (random.randint(0, 1) == 0)

    # the election object
    elename = "The " + capfirst(genword()) + " Election"
    desc = "Please " + genverb() + " " + gennoun() + ". Thank you."
    new_ele = Election(date_start=start, date_end=end, is_student=stud, name=elename, description=desc, are_notifs_generated=True)
    new_ele.save()
    now = datetime.datetime.now(tz)
    
    # logging of the creation
    if now < start:
        timestate = "not started"
    elif now > end:
        timestate = "already ended"
    else:
        timestate = "currently running"
        
    log("Created \"" + elename + "\"\t with id = " + str(new_ele.id) + ", is_student = " + str(stud) + ", date_start = " + str(start) + ", date_end = " + str(end) + " (" + timestate + ").")

    c1, c2, c3 = Candidate.objects.filter(is_student=stud).order_by('?').all()[:3]
    vot1 = vot2 = vot3 = 0

    # notifications are not yet generated for the election
    if (now < start or (now < end and random.randint(0, 2) == 0)):
        new_ele.are_notifs_generated = False
        new_ele.save()
        if now > start:
            log("This running election does not have generated notifications.")
    # notifications are alrady generated, some votes are casted
    else:
        # number of votes for each of the three candidates in this election
        vot1 = vot2 = vot3 = 0
        
        # this is a student election
        if (not stud):
            # all the notifications that should be created (notifications for parents, can relate to multiple students)
            notifs = bakalari_reader.get_all_youth_by_parent()

            for notif in notifs:
                issent = not (random.randint(0, 6) == 0)
                isused = False

                # the notification can only be used if it is already sent
                if issent:
                    isused = (random.randint(0, 1) == 0)
                    if isused:
                        for i in notif:
                            # choose a candidate for which to vote, or choose not to vote at all
                            val = random.randint(0, 3)
                            if val == 0:
                                vot1 += 1
                            elif val == 1:
                                vot2 += 1
                            elif val == 2:
                                vot3 += 1
                new_notification = Notification(election=new_ele, sent=issent, used=isused)
                new_notification.save()

                # add a vote object for each of the related students
                for idstud in notif:
                    new_vote = Vote(notification=new_notification, id_student=idstud)
                    new_vote.save()

        # this is not a student election
        else:
            # all the notifications that should be created (notifications for old enough students, each relates exactly to one student)
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
    
    # create and save the scores
    new_score1 = Score(election=new_ele, candidate=c1, votes=vot1)
    new_score2 = Score(election=new_ele, candidate=c2, votes=vot2)
    new_score3 = Score(election=new_ele, candidate=c3, votes=vot3)
    new_score1.save()
    new_score2.save()
    new_score3.save()

"""
Generates a string (a sentence) describing a generic candidate. Should be used as an annotation.
"""
def generateannotation():
    return "This candidate is " + genquality() + " and they live in " + capfirst(genword()) + "."
            
"""
Chooses a random first name from a predefined list. Should be used to generate candidate names.
"""
def genfirstname():
    names = ["Mike", "Elis", "Ellinor", "Ralph", "Eduard", "Emil", "Frederick", "Frederic", "Frederik", "Leopold", "Maria", "Anthony", "Anna", "Valeria", "Alexandra", "Sigmund", "Pawel", "Andrei", "Simon", "Lisa", "Paula", "Nell", "Barbara"]
    return names[random.randint(0, len(names) - 1)]

"""
Chooses a random grammatical modifier. Typically includes an adjective. Should be used to generate annotations.
"""
def genquality():
    qualities = ["good", "very smelly", "excellent", "meh", "bad", "terrible", "fine", "awesome", "nice to old men", "funny"]
    return qualities[random.randint(0, len(qualities) - 1)]

"""
Randomly generates a new candidate and adds them to the database.
"""
def addcandidate(stud):
    firstname = capfirst(genword()) + " " + genfirstname()
    lastname = capfirst(genword())
    annotation=generateannotation()
    new_cand = Candidate(name=firstname, surname=lastname, is_student=stud, annotation=annotation)
    new_cand.save()

# clearing databases

log("Deleting all candidates.")
Candidate.objects.all().delete()

log("Deleting all elections, votes, notifications.")
Election.objects.all().delete()
Vote.objects.all().delete()
Notification.objects.all().delete()

# adding new data

log("Creating new random candidates.")
for i in range(12):
    addcandidate(random.randint(0, 1) == 0)

log("Creating candidates some of which are required to be student, some non-student.")
for i in range(3):
    addcandidate(True)
    addcandidate(False)

log("Creating new elections: most of the already started ones also with votes and notifications.")
for i in range(7):
    start = datearoundnow()
    addnewelection(start, enddate(start))

for i in range(4):
    start = datetime.datetime.now(tz) + datetime.timedelta(days=random.randint(-3, -1))
    end = datetime.datetime.now(tz) + datetime.timedelta(days=random.randint(2, 5))
    addnewelection(start, end)

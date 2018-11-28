#!/usr/bin/env python
import os
import sys
import time
import random
import datetime

from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()
from api.models import Candidate, Election

def datearoundnow():
    return date(2018, 11, 30) + datetime.timedelta(days=random.randint(-20, 30))

def enddate(startdate):
    return startdate + datetime.timedelta(days=random.randint(2, 7))

def genvowel():
    vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'oe', 'ue', 'ae', 'ou']
    return vowels[random.randint(0, len(vowels) - 1)]

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

def genword():
    outstr = ""
    for i in range(3):
        outstr += genconsonant()
        outstr += genvowel()
    return outstr

def capfirst(word):
    return word[0].capitalize() + word[1:]

def addnewelection():
    start = datearoundnow()
    end = enddate(start)
    stud = (random.randint(0, 1) == 0)
    elename = "The " + capfirst(genword()) + " Election"
    desc = "Please " + genword() + " " + genword() + " " + genword() + ". Thank you."
    new_ele = Election(date_start=start, date_end=end, is_student=stud, name=elename, description=desc)
    new_ele.save()

# database override
Election.objects.all().delete()

for i in range(7):
    addnewelection()


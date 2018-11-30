import sqlite3
import datetime
from pytz import timezone
from django.conf import settings

tz = timezone(settings.TIME_ZONE)
conn = sqlite3.connect('bakalari.db')

"""
Finds and returns the email of the parent of the student identified by the given id in the bakalari database.
"""
def get_parent_email(student_id):
    return conn.cursor().execute("SELECT \"Parent Email\" FROM bakalari WHERE ID=(?);", [str(student_id)]).fetchone()[0]

"""
Finds and returns the email of the student identified by the given id in the bakalari database.
"""
def get_student_email(student_id):
    return conn.cursor().execute("SELECT Email FROM bakalari WHERE ID=(?);", [str(student_id)]).fetchone()[0]

"""
Returns ids of all underage students in the bakalari database grouped by parent emails.

Returns an array of arrays. Each subarray contains ids of students with a common parent email. No two ids from different subarrays have the same parent email.
"""
def get_all_youth_by_parent():
    now = datetime.datetime.now(tz)

    # underage students have birthday after (not at) this datetime
    dt = datetime.date(now.year - 18, now.month, now.day)

    # all students with non-empty parent email and birthdate ordered by parent email
    students = conn.cursor().execute("SELECT ID, Birthdate, \"Parent Email\" FROM bakalari WHERE \"Parent Email\" <> \"\" AND Birthdate <> \"\" ORDER BY \"Parent Email\";").fetchall()

    # adult students filtered out
    filtered = []
    for stud in students:
        day, month, year = map(int, stud[1].split('.'))
        birthdate = datetime.date(year, month, day)
        if dt < birthdate:
            filtered.append(stud)

    
    # 
    notifs = []
    last = 0
    for i in range(len(filtered)):
        if (i == len(filtered) - 1 or filtered[i][2] != filtered[i + 1][2]):
            notifs.append([filtered[x][0] for x in range(last, i + 1)])
            last = i + 1
    return notifs


def get_all_oldenough():
    now = datetime.datetime.now()
    dt = datetime.date(now.year - 18, now.month, now.day)
    students = conn.cursor().execute("SELECT ID, Birthdate FROM bakalari WHERE \"Email\" <> \"\" AND Birthdate <> \"\";").fetchall()
    notifs = []
    for stud in students:
        day, month, year = map(int, stud[1].split('.'))
        birthdate = datetime.date(year, month, day)
        if dt >= birthdate:
            notifs.append(stud[0])
    return notifs


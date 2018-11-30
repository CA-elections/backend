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

    
    # notif - an array of student ids with the same parent email
    notifs = []
    # the first index in the filtered array with the current parent email
    first = 0
    for i in range(len(filtered)):
        if (i == len(filtered) - 1 or filtered[i][2] != filtered[i + 1][2]):
            notifs.append([filtered[x][0] for x in range(first, i + 1)])
            first = i + 1
    return notifs

"""
Returns ids of all adult students in the bakalari database in a plain array.
"""
def get_all_oldenough():
    now = datetime.datetime.now(tz)

    # adult students have birthday before or at this datetime
    dt = datetime.date(now.year - 18, now.month, now.day)

    # all students with non-empty email and birthdate
    students = conn.cursor().execute("SELECT ID, Birthdate FROM bakalari WHERE \"Email\" <> \"\" AND Birthdate <> \"\";").fetchall()

    # filter only ids of adult students
    notifs = []
    for stud in students:
        day, month, year = map(int, stud[1].split('.'))
        birthdate = datetime.date(year, month, day)
        if dt >= birthdate:
            notifs.append(stud[0])
    return notifs


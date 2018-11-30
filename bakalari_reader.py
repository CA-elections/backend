import sqlite3
import datetime
from pytz import timezone
from django.conf import settings

tz = timezone(settings.TIME_ZONE)
conn = sqlite3.connect('bakalari.db')

def get_parent_email(student_id):
    return conn.cursor().execute("SELECT \"Parent Email\" FROM bakalari WHERE ID=(?);", [str(student_id)]).fetchone()[0]


def get_student_email(student_id):
    return conn.cursor().execute("SELECT Email FROM bakalari WHERE ID=(?);", [str(student_id)]).fetchone()[0]


def get_birthdate(student_id):
    day, month, year = map(int, conn.cursor().execute("SELECT Birthdate FROM bakalari WHERE ID=(?);",
                                                      [str(student_id)]).fetchone()[0].split("."))
    return datetime.date(year, month, day)


def get_infants_with_parent_email(parent_email):
    now = datetime.datetime.now(tz)
    dt = datetime.date(now.year - 18, now.month, now.day)
    for i, birth in conn.cursor().execute("SELECT ID, Birthdate FROM bakalari WHERE \"Parent Email\"=(?);", [parent_email]):
        day, month, year = map(int, birth.split('.'))
        birthdate = datetime.date(year, month, day)
        if dt <= birthdate:
            yield i


def get_students_with_parent_email(parent_email):
    yield from map(int, map(lambda x: x[0], conn.cursor().execute("SELECT ID FROM bakalari WHERE \"Parent Email\"=(?);",
                                                                  [parent_email])))


def get_students():
    yield from map(int, map(lambda x: x[0], conn.cursor().execute("SELECT ID FROM bakalari;")))


def get_all_youth_by_parent():
    now = datetime.datetime.now()
    dt = datetime.date(now.year - 18, now.month, now.day)
    students = conn.cursor().execute("SELECT ID, Birthdate, \"Parent Email\" FROM bakalari WHERE \"Parent Email\" <> \"\" AND Birthdate <> \"\" ORDER BY \"Parent Email\";").fetchall()
    filtered = []
    for stud in students:
        day, month, year = map(int, stud[1].split('.'))
        birthdate = datetime.date(year, month, day)
        if dt < birthdate:
            filtered.append(stud)

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


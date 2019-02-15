#import sqlite3
import pyodbc
import datetime
from pytz import timezone
from django.conf import settings

tz = timezone(settings.TIME_ZONE)
"""
cursor.execute("select zaci_zzd.PRIJMENI from zaci join zaci_zzr on zaci.INTERN_KOD=zaci_zzr.INTERN_KOD join zaci_zzd on zaci_zzr.ID_ZZ=zaci_zzd.ID where zaci.JMENO='Tomáš' and zaci.PRIJMENI='Hozda' and zaci_zzr.JE_ZZ='1'").fetchone()
"""

# | Doplnit údaje sem
# v
conn = pyodbc.connect('DSN=MySQLServerDatabase;UID=uzivatelske_jmeno;PWD=heslo_uzivatele')
# ^
# | Doplnit údaje sem


"""
Finds and returns the email of the parent of the student identified by the given id in the bakalari database.
"""
def get_parent_email(student_id):
    return cursor.execute("""
        SELECT
            zaci_zzd.E_MAIL
        FROM
            zaci
        JOIN
            zaci_zzr
            ON
            zaci.INTERN_KOD=zaci_zzr.INTERN_KOD
        JOIN
            zaci_zzd
            ON
            zaci_zzr.ID_ZZ=zaci_zzd.ID
        WHERE
            zaci.INTERN_KOD=(?)
        AND
            zaci_zzr.JE_ZZ=1;""", [str(student_id)]).fetchone()[0]

"""
Finds and returns the email of the student identified by the given id in the bakalari database.

x
"""
def get_student_email(student_id):
    cursor = con.cursor()
    cursor.execute('use bakalari_data')
    return cursor.execute("SELECT E_MAIL FROM zaci WHERE INTERN_KOD=(?);", [str(student_id)]).fetchone()[0]

"""
Returns ids of all underage students in the bakalari database grouped by parent emails.

Returns an array of arrays. Each subarray contains ids of students with a common parent email. No two ids from different subarrays have the same parent email.
"""
def get_all_youth_by_parent():
    cursor = con.cursor()
    cursor.execute('use bakalari_data')
    now = datetime.datetime.now(tz)

    # underage students have birthday after (not at) this datetime
    dt = datetime.date(now.year - 18, now.month, now.day)

    # all students with non-empty parent email and birthdate ordered by parent email
    students = cursor.execute("""
        SELECT
            zaci.INTERN_KOD,
            zaci.DATUM_NAR,
            zaci_zzd.E_MAIL
        FROM
            zaci
        JOIN
            zaci_zzr
            ON
            zaci.INTERN_KOD=zaci_zzr.INTERN_KOD
        JOIN
            zaci_zzd
            ON
            zaci_zzr.ID_ZZ=zaci_zzd.ID
        WHERE
            TRIM(zaci_zzd.E_EMAIL) IS NOT NULL
        AND
            TRIM(zaci.DATUM_NAR) IS NOT NULL
        ORDER BY
            zaci_zzd.EMAIL;""").fetchall()

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
    cursor = con.cursor()
    cursor.execute('use bakalari_data')
    now = datetime.datetime.now(tz)

    # adult students have birthday before or at this datetime
    dt = datetime.date(now.year - 18, now.month, now.day)

    # all students with non-empty email and birthdate
    students = cursor.execute("""
        SELECT
            INTERN_KOD,
            DATUM_NAR
        FROM
            zaci
        WHERE
            TRIM(E_MAIL) IS NOT NULL
        AND
            TRIM(DATUM_NAR) IS NOT NULL;""").fetchall()

    # filter only ids of adult students
    notifs = []
    for stud in students:
        day, month, year = map(int, stud[1].split('.'))
        birthdate = datetime.date(year, month, day)
        if dt >= birthdate:
            notifs.append(stud[0])
    return notifs


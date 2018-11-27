import sqlite3
import datetime
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
    now = datetime.datetime.now()
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


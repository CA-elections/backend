import sqlite3
import datetime
conn = sqlite3.connect('bakalari.db')


def get_parent_email(student_id):
    return conn.cursor().execute("SELECT \"Parent Email\" FROM bakalari WHERE ID=(?);", [str(student_id)]).fetchone()[0]


def get_birthdate(student_id):
    return datetime.date(*(conn.cursor().execute("SELECT Birthdate FROM bakalari WHERE ID=(?);", [str(student_id)]).fetchone()[0].split(".")))


def get_students_with_parent_email(parent_email):
    yield from map(int, map(lambda x: x[0], conn.cursor().execute("SELECT ID FROM bakalari WHERE \"Parent Email\"=(?);", [parent_email])))


def get_students():
    yield from map(int, map(lambda x: x[0], conn.cursor().execute("SELECT ID FROM bakalari;")))


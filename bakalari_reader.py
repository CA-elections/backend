import sqlite3
conn = sqlite3.connect('bakalari.db')


def get_parent_email(student_id):
    return conn.cursor().execute("SELECT Parent Email FROM bakalari WHERE ID=(?);", str(student_id)).fetchone()[0]


def get_birthdate(student_id):
    return conn.cursor().execute("SELECT Birthdate FROM bakalari WHERE ID=(?);", str(student_id)).fetchone()[0]


def get_students():
    yield from map(int, map(lambda x: x[0], conn.cursor().execute("SELECT ID FROM bakalari;")))


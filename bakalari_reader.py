import sqlite3
conn = sqlite3.connect('file:/bakalari.db?mode=ro', uri=True)


def get_parent_email(student_id):
    return conn.cursor().execute("SELECT 'Parent Email' FROM bakalari WHERE ID=(?);", student_id).fetchone()[0]


def get_birthdate(student_id):
    return conn.cursor().execute("SELECT Birthdate FROM bakalari WHERE ID=(?);", student_id).fetchone()[0]


def get_students():
    yield from conn.cursor().execute("SELECT ID FROM bakalari;")


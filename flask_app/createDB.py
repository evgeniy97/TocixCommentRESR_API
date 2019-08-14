import sqlite3
import os

PATH = "commentDB.sqlite"

if os.path.exists(PATH):
    os.remove(PATH)

conn = sqlite3.connect(PATH)
c = conn.cursor()

c.execute('CREATE TABLE comment_db (comment TEXT, toxic INTEGER, date TEXT)')

conn.commit()
conn.close()
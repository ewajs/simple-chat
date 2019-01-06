import sqlite3
from datetime import datetime

from flask import g

DATABASE = 'test.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def save_msg(msg_text: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO Message (Date, UserID, MessageText) VALUES (?, 0, ?)",
              (datetime.utcnow().replace(microsecond=0).isoformat(),
               msg_text))
    conn.commit()

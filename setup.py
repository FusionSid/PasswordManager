import sqlite3
from utils import *

password = input("PASSWORD: ")
password = encrypt(password)

with sqlite3.connect("utils/database/main.db") as db:
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        password TEXT
    )""")

    cur.execute(f"INSERT INTO Profiles (name, password) VALUES ('master', '{password}')")

    db.commit()

with sqlite3.connect("utils/database/passwords.db") as db:
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        password TEXT,
        profile INTEGER
    )""")
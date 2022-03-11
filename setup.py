import sqlite3
import random
from utils import *

SALT = input("Type something random here for the salt: ")
ITERATIONS = random.randint(100000, 1000000)

with open(".env", "w") as f:
    f.write(f"SALT = {SALT}\nITERATIONS = {ITERATIONS}")

password = input("Set password for master Profile: ")
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

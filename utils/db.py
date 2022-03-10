import sqlite3
from typing import *
from .encrypt import *

def get_key() -> str:
    with sqlite3.connect("utils/database/main.db") as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM Profiles")

    data = cur.fetchall()
    key = encrypt(data[0][2]).encode()
    key = base64.b64encode(SHA256.new(key).digest())

    return key


def get_db() -> List:
    with sqlite3.connect("utils/database/passwords.db") as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM Passwords")

    data = cur.fetchall()

    return list(data)


def get_main_db() -> List:
    with sqlite3.connect("utils/database/main.db") as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM Profiles")

    data = cur.fetchall()

    return data


def insert_password(name : str, password : str, profile : int) -> bool:
    key = get_key()
    password = password.encode()
    encrypted_password = encrypt_password(key, password)
    # try:
    with sqlite3.connect("utils/database/passwords.db") as db:
        cur = db.cursor()
        cur.execute("INSERT INTO Passwords (name, password, profile) VALUES (?, ?, ?)", (name, encrypted_password, profile))
        
        db.commit()

    return True

    # except Exception as err:
    #     print(err)
    #     return False

def get_profile(number):
    with sqlite3.connect("utils/database/passwords.db") as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM Passwords WHERE profile={number}")
        data = cur.fetchall()
    return data
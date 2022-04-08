from Crypto.Hash import SHA256

import base64
import sqlite3
from .encrypt import encrypt, encrypt_password


cwd = "/Users/siddheshzantye/Desktop/Coding/Python/Password-Manager/" # if youre running the script in this file then leave this as "", but if you running this from another folder, put the full path in there and make sure it ends with a /


def get_key() -> str:
    """
    Generates a key

    Returns
        str : The key
    """
    with sqlite3.connect(f"{cwd}utils/database/main.db") as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM Profiles")

    data = cur.fetchall()
    key = encrypt(data[0][2]).encode()
    key = base64.b64encode(SHA256.new(key).digest())

    return key


def get_db() -> list:
    """
    Returns the whole db file
    """
    with sqlite3.connect(f"{cwd}utils/database/passwords.db") as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM Passwords")

    data = cur.fetchall()

    return list(data)


def get_main_db() -> list:
    """
    Returns the whole main db file
    """
    try:
        with sqlite3.connect(f"{cwd}utils/database/main.db") as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM Profiles")

        data = cur.fetchall()

        return data
    except Exception as e:
        print(f"ERROR: {e}\nNo table found\nPlease run setup.py first")
        quit()


def insert_password(name : str, password : str, profile : int) -> bool:
    """
    Inserts a password into an account

    Parameters
        :param name (str): The name of the password
        :param password (str): The password
        :param profile (int): The number of the profile
    """
    key = get_key()
    password = password.encode()
    encrypted_password = encrypt_password(key, password)
    with sqlite3.connect(f"{cwd}utils/database/passwords.db") as db:
        cur = db.cursor()
        cur.execute("INSERT INTO Passwords (name, password, profile) VALUES (?, ?, ?)", (name, encrypted_password, profile))
        
        db.commit()


def get_profile(number : int) -> list:
    """
    Gets a profile with an id

    Parameters
        :param number (int) : The profiles number
    """
    with sqlite3.connect(f"{cwd}utils/database/passwords.db") as db:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM Passwords WHERE profile={number}")
        data = cur.fetchall()
    return data
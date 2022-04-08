import random
import sqlite3

from getpass import getpass
from rich.console import Console
from rich.prompt import Prompt

from utils import encrypt

console = Console()

SALT = Prompt.ask("[red]Type something random here for the salt")
ITERATIONS = random.randint(100000, 1000000)

with open(".env", "w") as f:
    f.write(f"SALT = {SALT}\nITERATIONS = {ITERATIONS}")

console.print("[blue]Set password for master profile: ", end="")
password = getpass("")
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

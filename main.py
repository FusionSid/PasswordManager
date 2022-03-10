from utils import *

profiles = get_main_db()

if len(profiles) == 1:
    correct_password = profiles[0][2]

    tries = 0
    
    while True:
        password = input(f"Enter password for {profiles[0][1]}: ")
        password = encrypt(password)

        if password == correct_password:
            break
        print("Wrong Password")
        tries += 1

        if tries >= 3:
            print("Out of tries")
            break

print("insert? or get?")

iorg = input("(i/g): ")

if iorg == "g":
    database = get_db()
    for i in database:
        print(i)
        print(f"Name: {i[1]}\nPassword: {i[2]}")
        print("Decryted:", (decrypt_password(get_key(), i[2])).decode())

if iorg == "i":
    name = input("Name: ")
    password = input("Password: ")
    insert_password(name, password, 1)

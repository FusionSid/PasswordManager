from utils import *

profiles = get_main_db()

# iorg = input("(i/g): ")

# if iorg == "g":
#     database = get_db()
#     print(database)
#     database = database[profile_number-1]
#     for i in database:
#         print(f"Name: {i[1]}\nPassword: {i[2]}")
#         print("Decryted:", (decrypt_password(get_key(), i[2])).decode())

# if iorg == "i":
#     name = input("Name: ")
#     password = input("Password: ")
#     insert_password(name, password, 1)




def login():
    profile_name_list = '\n'.join([f"{p} : {i[1]}" for p, i in enumerate(profiles)])
    print(f"\nLogin\n-----\n\nProfiles:\n{profile_name_list}\n\n")
    print("Enter Profile Number:")

    try:
        profile_number = int(input("> "))
        if profile_number+1 > len(profiles):
            print("To high")
        elif profile_number < 0:
            print("Must be 0 or more")
    except ValueError:
        print("Must be an int")
        
    profile = profiles[profile_number]
    correct_password = profile[2]
    tries = 0

    # passwords = get_profile(profile_number+1)

    while True:
        password = input(f"Enter password for {profile[1]}: ")
        password = encrypt(password)

        if password == correct_password:
            profile_number = profile[0]
            print("Correct")
            break
        print(f"Wrong Password! ({3 - tries} attempts remaining)")
        tries += 1

        if tries >= 4:
            print("Out of tries")
            break
    
    return profile


def logged_in(key, num):
    while True:
        profile = get_profile(num)
        do = input("\nWhat would you like to do?\nOptions:\nl or logout - to logout\ng or get - to get passwords\nf or find - to find specific password\ni to insert - To add a new password\n> ")

        if do.lower() in ["i", "insert"]:
            name = input("Enter the name of the password: ")
            password = input("Enter the password: ")
            insert_password(name, password, num)

        elif do.lower() in ["g", "get"]:
            if profile is None or len(profile) == 0:
                print("You don't have anything stored")
            else:
                print(profile)
                for i in profile:
                    password = decrypt_password(key, i[2]).decode()
                    print(f"\nName: {i[1]}\nPassword: {password}\n")
        
        elif do.lower() in ["f", "find"]:
            pass

        elif do.lower() in ["l", "logout"]:
            return

        else:
            print("Invalid Option")

while True:
    do = input("\nWhat would you like to do?\nOptions:\nl or login - to login\nc to create - To create a new profile\nq or quit - To quit\n> ")

    if do.lower() in ["l", "login"]:
        log = login()
        profile = get_profile(log[0])
        key = get_key()
        logged_in(key, log[0])

    elif do.lower() in ["c", "create"]:
        print("ok")

    elif do.lower() in ["q", "quit"]:
        quit()

    else:
        print("Invalid Option")
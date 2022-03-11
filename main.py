from utils import *
import pyfiglet
import time
import os

os.system("clear")
print(pyfiglet.figlet_format("Password Manager"))

COLORS = {
    # Colors
    "red": "\033[91m",
    "yellow": "\033[93m",
    "green": "\033[92m",
    "blue": "\033[94m",
    "cyan": "\033[96m",
    "magenta": "\u001b[35m",
    "purple": "\033[95m",
    "black": "\u001b[30m",
    # Effects
    "reset": "\u001b[0m",
    "bold": "\033[1m",
    "underline": "\033[4m",
}

profiles = get_main_db()

divider = "-----------------------------------------------------------------------------------------------------------------------\n"

lockImg = f"""{COLORS["red"]}                               
                                   
                                                          ^jEQBQDj^             
                                                       r#@@@@@@@@@#r           
                                                       ?@@@#x_`_v#@@@x          
                                                       g@@@!     !@@@Q          
                                                       Q@@@_     _@@@B          
                                                    rgg@@@@QgggggQ@@@@ggr       
                                                    Y@@@@@@@@@@@@@@@@@@@Y       
                                                    Y@@@@@@@Qx^xQ@@@@@@@Y       
                                                    Y@@@@@@@^   ~@@@@@@@Y       
                                                    Y@@@@@@@@r r#@@@@@@@Y       
                                                    Y@@@@@@@@c,c@@@@@@@@Y       
                                                    Y@@@@@@@@@@@@@@@@@@@Y       
                                                    v###################v       
                                                   
                                                                
    {COLORS["reset"]}"""

checkImg = f"""{COLORS["green"]}                               
                                   
                                                                       `xx.  
                                                                     'k#@@@h`
                                                                   _m@@@@@@Q,
                                                                 "M@@@@@@$*  
                                                 `xk<          =N@@@@@@9=    
                                                T#@@@Qr      ^g@@@@@@5,      
                                                y@@@@@@Bv  ?Q@@@@@@s-        
                                                `V#@@@@@#B@@@@@@w'          
                                                    `t#@@@@@@@@#T`            
                                                      vB@@@@Bx               
                                                        )ER)                            
                                                                                                       
    {COLORS['reset']}"""


print(lockImg)

def login():
    os.system("clear")
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

    while True:
        password = input(f"Enter password for {profile[1]}: ")
        password = encrypt(password)

        if password == correct_password:
            profile_number = profile[0]
            print(checkImg)
            for i in range(3):
                time.sleep(0.3)
                print("Loading Account .  ", end="\r")
                time.sleep(0.3)
                print("Loading Account .. ", end="\r")
                time.sleep(0.3)
                print("Loading Account ...", end="\r")
                time.sleep(0.3)
                print("Loading Account    ", end="\r")
            break
        print(f"{COLORS['red']}Wrong Password! ({3 - tries} attempts remaining){COLORS['reset']}")
        tries += 1

        if tries >= 4:
            print("Out of tries")
            quit()
    
    return profile


def logged_in(key, num):
    os.system("clear")
    while True:
        profile = get_profile(num)
        do = input(f"{COLORS['yellow']}\nWhat would you like to do?\nOptions:\nl or logout - to logout\ng or get - to get passwords\nf or find - to find specific password\ni to insert - To add a new password\n> ")

        if do.lower() in ["i", "insert"]:
            name = input("Enter the name of the password: ")
            password = input("Enter the password: ")
            insert_password(name, password, num)

        elif do.lower() in ["g", "get"]:
            if profile is None or len(profile) == 0:
                print("You don't have anything stored")
            else:
                print(divider)
                for i in profile:
                    password = decrypt_password(key, i[2]).decode()
                    print(f"\nID: {i[0]}\nName: {i[1]}\nPassword: {password}\n")
                print(divider)
        
        elif do.lower() in ["f", "find"]:
            search_type = int(input("Search Type:\n\n0: ID\n1: Name\n\nType 0 or 1\n> "))
            found = False

            if search_type == 0:
                _id = int(input("Enter ID: "))
                for i in profile:
                    if i[0] == _id:
                        found = True
                        password = decrypt_password(key, i[2]).decode()
                        print(f"\nID: {i[0]}\nName: {i[1]}\nPassword: {password}\n")
                if found == False:
                    print("Not found")


            if search_type == 1:
                name = input("Enter name: ")
                for i in profile:
                    if i[1].lower() == name.lower():
                        found = True
                        password = decrypt_password(key, i[2]).decode()
                        print(f"\nID: {i[0]}\nName: {i[1]}\nPassword: {password}\n")
                if found == False:
                    print("Not found")


        elif do.lower() in ["l", "logout"]:
            return

        else:
            print("Invalid Option")

while True:
    do = input(f"{COLORS['cyan']}\nWhat would you like to do?\nOptions:\nl or login - to login\nc to create - To create a new profile\nq or quit - To quit\n> {COLORS['reset']}")

    if do.lower() in ["l", "login"]:
        log = login()
        profile = get_profile(log[0])
        key = get_key()
        logged_in(key, log[0])

    elif do.lower() in ["c", "create"]:
        name = input("Enter profile name: ")
        password = encrypt(input("ENTER PASSWORD: "))
        with sqlite3.connect("utils/database/main.db") as db:
            cur = db.cursor()
            cur.execute(f"INSERT INTO Profiles (name, password) VALUES ('{name}', '{password}')")

            db.commit()
        
        print(f"Profile {name} Created!")

    elif do.lower() in ["q", "quit"]:
        quit()

    else:
        print("Invalid Option")

    os.system("clear")
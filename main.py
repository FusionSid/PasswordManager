import os
import asyncio

import pyfiglet
import aiosqlite

import clipboard
from getpass import getpass

from rich.table import Table
from rich.progress import track
from rich.console import Console
from rich.traceback import install
from rich.prompt import Prompt, Confirm

import utils
from utils.ascii_art import lockImg, divider, checkImg


install()
console = Console()
profiles = utils.get_main_db()


async def login():
    os.system("clear")
    console.print(f"[green]{divider}")

    table = Table(title="\n[blue]Profiles:")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Profile Name:", justify="center", style="cyan", no_wrap=True)
    for index, _profile in enumerate(profiles):
        table.add_row(str(index), _profile[1])

    console.print(table)

    console.print("\n[blue]Enter Profile Number:")
    profile_number = None

    while True:
        try:
            profile_number = int(Prompt.ask(""))

            if profile_number + 1 > len(profiles):
                console.print("[red]Profile number to high")
            elif profile_number < 0:
                console.print("[red]Must be 0 or more")
            else:
                break

        except ValueError:
            console.print("[red] Profile number must be an int")

    profile = profiles[profile_number]
    correct_password = profile[2]
    tries = 0

    while True:
        password = getpass(f"Enter password for {profile[1]}: ")
        password = utils.encrypt(password)

        if password == correct_password:
            profile_number = profile[0]
            console.print(f"[green]{divider}")
            console.print(f"[green]{checkImg}")
            console.print(f"[green]{divider}\n")

            async def process_data():
                await asyncio.sleep(0.02)

            for _ in track(range(100), description="[green]Loading Account"):
                await process_data()
            break
        console.print(f"[red]Wrong Password! ({3 - tries} attempts remaining)")
        tries += 1

        if tries >= 4:
            print("Out of tries")
            quit()
    os.system("clear")
    return profile


async def logged_in(key, num):
    os.system("clear")
    while True:
        profile = utils.get_profile(num)
        table = await get_logged_in_options()
        console.print(table)
        what_to_do = Prompt.ask(f"[yellow]What would you like to do?", default="get")

        if what_to_do == "i" or what_to_do == "insert":
            name = input("Enter the name of the password: ")
            console.print("[blue]Enter the password:", end=" ")
            password = getpass("")
            utils.insert_password(name, password, num)

        elif what_to_do == "f" or what_to_do == "find":
            search_type_table = Table(title="Search Types:")
            search_type_table.add_column(
                "Number:", justify="center", style="cyan", no_wrap=True
            )
            search_type_table.add_column(
                "Type:", justify="center", style="cyan", no_wrap=True
            )
            search_type_table.add_row("0", "ID Search")
            search_type_table.add_row("1", "Name Search")
            console.print(search_type_table)
            search_type = int(Prompt.ask("[blue]Enter search type", default=1))

            found = False
            if search_type == 0:
                data_table = Table(title="Info")
                data_table.add_column(
                    "ID:", justify="center", style="cyan", no_wrap=True
                )
                data_table.add_column(
                    "Name:", justify="center", style="cyan", no_wrap=True
                )
                data_table.add_column(
                    "Password:", justify="center", style="cyan", no_wrap=True
                )

                _id = int(Prompt.ask("[blue]Enter ID"))
                for i in profile:
                    if i[0] == _id:
                        found = True
                        console.print(f"[green]{divider}")

                        password = utils.decrypt_password(key, i[2]).decode()
                        data_table.add_row(str(i[0]), i[1], password)
                        console.print(data_table)
                        copy = Confirm.ask("Copy to clipboard?")
                        if copy:
                            clipboard.copy(password)
                        console.print(f"[green]{divider}")

                if found == False:
                    print("Not found")

            if search_type == 1:
                data_table = Table(title="Info")
                data_table.add_column(
                    "ID:", justify="center", style="cyan", no_wrap=True
                )
                data_table.add_column(
                    "Name:", justify="center", style="cyan", no_wrap=True
                )
                data_table.add_column(
                    "Password:", justify="center", style="cyan", no_wrap=True
                )

                name = Prompt.ask("[blue]Enter name")
                for i in profile:
                    if i[1].lower() == name.lower():
                        found = True
                        console.print(f"[green]{divider}")
                        password = utils.decrypt_password(key, i[2]).decode()
                        data_table.add_row(str(i[0]), i[1], password)
                        console.print(data_table)
                        copy = Confirm.ask("Copy to clipboard?")
                        if copy:
                            clipboard.copy(password)
                        console.print(f"[green]{divider}")

                if found == False:
                    print("Not found")

        elif what_to_do == "g" or what_to_do == "get":
            if profile is None or len(profile) == 0:
                print("You don't have anything stored")
                Prompt.ask("[yellow]Press any key to continue ")
                os.system("clear")
                continue

            console.print(f"[green]{divider}")

            data_table = Table(title="Info")
            data_table.add_column("ID:", justify="center", style="cyan", no_wrap=True)
            data_table.add_column("Name:", justify="center", style="cyan", no_wrap=True)
            data_table.add_column(
                "Password:", justify="center", style="cyan", no_wrap=True
            )

            for pswd_set in profile:
                password = utils.decrypt_password(key, pswd_set[2]).decode()
                data_table.add_row(str(pswd_set[0]), pswd_set[1], password)

            console.print(data_table)

            console.print(f"[green]{divider}")

        elif what_to_do == "l" or what_to_do == "logout":
            return

        else:
            table = await get_logged_in_options()
            console.print(table)

        Prompt.ask("[yellow]Press any key to continue ")
        os.system("clear")


async def create_new_account():
    name = Prompt.ask("[blue]Enter profile name[/]")
    console.print("[blue]Enter password:", end=" ")
    password = utils.encrypt(getpass(""))

    async with aiosqlite.connect("utils/database/main.db") as db:
        await db.execute(
            f"INSERT INTO Profiles (name, password) VALUES ('{name}', '{password}')"
        )
        await db.commit()

    console.print(f"[green]Profile {name} Created!")


async def get_options():
    table = Table(title="\n[bold red]Options")

    table.add_column("Command", justify="center", style="cyan", no_wrap=True)
    table.add_column("Usage", justify="center", style="cyan", no_wrap=True)
    table.add_row(
        "Create a profile",
        "c or create",
    )
    table.add_row(
        "Login",
        "l or login",
    )
    table.add_row("Quit the program", "q or quit")

    return table


async def get_logged_in_options():
    table = Table(title="\n[bold red]Options")

    table.add_column("Command", justify="center", style="cyan", no_wrap=True)
    table.add_column("Usage", justify="center", style="cyan", no_wrap=True)
    table.add_row(
        "Get password",
        "g or get",
    )
    table.add_row(
        "Logout",
        "l or logout",
    )
    table.add_row(
        "Find password",
        "f or find",
    )
    table.add_row("Insert password", "i or insert")

    return table


# Main loop / Script

os.system("clear")

console.print(f"[green]{divider}")
console.print(f"[green]{lockImg}")
console.print(f"[green]{divider}")


async def main():
    await asyncio.sleep(1.5)
    console.print(f"[bold blue]{pyfiglet.figlet_format('Password Manager')}")
    console.print((await get_options()))
    while True:
        what_to_do = Prompt.ask("\nWhat would you like to do?", default="login").lower()

        if what_to_do == "l" or what_to_do == "login":
            log = await login()
            utils.get_profile(log[0])
            key = utils.get_key()
            await logged_in(key, log[0])

        elif what_to_do == "c" or what_to_do == "create":
            await create_new_account()
            continue

        elif what_to_do == "q" or what_to_do == "quit":
            sure_quit = Confirm.ask("Are you sure you want to quit?")
            if sure_quit:
                quit()
            continue

        else:
            console.print("[red]Invalid Option!")
            table = await get_options()
            console.print(table)
            continue


loop = asyncio.new_event_loop()
loop.run_until_complete(main())

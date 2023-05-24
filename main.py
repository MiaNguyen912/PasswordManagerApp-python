import random
from tkinter import *
from tkinter import messagebox
import pyperclip  # allow to put string into the clipboard
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]  # password has number of letter in range (8,10)
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)  # shuffle the list and store result in that list

    password = "".join(password_list)  # join every item in list separated by ""

    password_box.delete(0, END)  # clear the field
    password_box.insert(0, password)

    pyperclip.copy(password)  # copy password into clipboard, so that we can use cmd+v to paste it to the website


# ---------------------------- SAVE AND FIND PASSWORD ------------------------------- #


def save():
    website = website_box.get()
    username = username_box.get()
    password = password_box.get()

    if len(website.strip()) == 0 or len(username.strip()) == 0 or len(password.strip()) == 0:  # if a field is empty or contains all space
        messagebox.showwarning(title="Oops", message="Do not leave any field empty!")
        return

    new_info = {website: {"username": username, "password": password}}  # json format

    is_confirmed = messagebox.askokcancel(title=website, message=f"Confirm: \nUsername: {username}\nPassword: {password}")
    if is_confirmed:
        try:
            with open("login_info.json", "r") as login_file:
                info = json.load(login_file)  # read old data
        except FileNotFoundError:
            with open("login_info.json", "w") as login_file:
                json.dump(new_info, login_file, indent=4)  # save new data
        else:
            info.update(new_info)  # update old data to new data
            with open("login_info.json", "w") as login_file:
                json.dump(info, login_file, indent=4)  # save new data
        finally:
            website_box.delete(0, END)
            password_box.delete(0, END)


def search():
    website = website_box.get()
    if len(website.strip()) == 0:
        messagebox.showwarning(title="Oops", message="Please enter the website name.")
        return

    try:
        with open("login_info.json", "r") as login_file:
            info = json.load(login_file)  # read data
            found_info = info[website]
    except FileNotFoundError:
        messagebox.showwarning(title="Oops", message=f"Cannot find any account associated with {website}.")
    except KeyError:
        messagebox.showwarning(title="Oops", message=f"Cannot find any account associated with {website}.")
    else:
        found_username = found_info["username"]
        found_password = found_info["password"]
        messagebox.showinfo(title=f"{website}", message=f"Username: {found_username}\nPassword: {found_password}")
    finally:
        website_box.delete(0, END)
        password_box.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")
window.minsize(width=200, height=200)

# logo canvas
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
logo_img = canvas.create_image(100, 100, image=logo)
canvas.grid(column=2, row=1)

# website line
website_label = Label(text="Website:", font=("Ariel", 15, "bold"))
website_label.grid(column=1, row=2)

website_box = Entry(width=21)
website_box.grid(column=2, row=2)
website_box.focus()  # automatically focus on this text box when window is opened

search_button = Button(text="Search", width=11, command=search)
search_button.grid(column=3, row=2)

# username line
username_label = Label(text="Email/Username:", font=("Ariel", 15, "bold"))
username_label.grid(column=1, row=3)

username_box = Entry(width=36)
username_box.grid(column=2, row=3, columnspan=2)
username_box.insert(END, "nguyendanlinh9122000@gmail.com")  # END is tkinter const, indicate the last character inside the entry

# password line
password_label = Label(text="Password:", font=("Ariel", 15, "bold"))
password_label.grid(column=1, row=4)

password_box = Entry(width=21)
password_box.grid(column=2, row=4, columnspan=1)


generate_button = Button(text="Generate Password", width=11, command=generate_password)
generate_button.grid(column=3, row=4, columnspan=1)

# add button
add_button = Button(text="Add", width=34, command=save)
add_button.grid(column=2, row=5, columnspan=2)

window.mainloop()

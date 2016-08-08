#!/usr/bin/env python3
'''
This little script is a simple password manager.
You give in your master password and the service you are using and based on this you get a some passwords.
'''
import hashlib
import base64
import getpass
import datetime
import sqlite3

ALPHABET = ('abcdefghijklmnopqrstuvwxyzäöü'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'
            '0123456789!@#$%^&*()-_')
ALPHABET_EXTENDED = ('abcdefghijklmnopqrstuvwxyzäöü'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'
            '0123456789!"§$%&/()=?*+#.:,;-_')
PASSW_LENGTH = 20

def print_table(row):
    print("{0:3} | {1:20} | {2:10} | {3:10}".format(row[0], row[1], row[2], row[3]))

def date_today():
    now = datetime.datetime.now()
    date = str(now.day) + "." + str(now.month) + "." + str(now.year)

    return date

def generate_extended_password(alpha, passw):
    # Convert the hexdigest into decimal
    num = int(passw, 16)

    num_chars = len(alpha) # base to convert num
    chars = []

    # generate new password, one digit at a time up to password length
    while len(chars) < PASSW_LENGTH:
        num, index = divmod(num, num_chars)
        chars.append(alpha[index])

    return chars

if __name__ == "__main__":
    try:
        # Open the db or create if not exists
        conn = sqlite3.connect("pwm.db") # pwm = passwordmanager

        # create table if not exists
        conn.execute('''CREATE TABLE IF NOT EXISTS SERVICES
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        service TEXT NOT NULL,
        version INT DEFAULT 1,
        updated TEXT NOT NULL,
        UNIQUE(service));''')
        # service is the name of the service, version is a number so password can be changed without changing service name (to-do), created is a time string when it was last updated

        # Show all services stored in db
        cursor = conn.execute("SELECT id, service, version, updated from SERVICES")

        print_table(["ID", "SERVICE", "VERSION", "UPDATED"])
        for row in cursor:
            print_table(row)

        # Ask for master password and used service
        master = getpass.getpass("Master password: ").encode("utf-8") # hides user input

        service = getpass.getpass("Login credentials: ").encode("utf-8").lower()
        prim_passw = master+service

        conn.execute("INSERT OR IGNORE INTO SERVICES (service, updated) VALUES(\"{}\", \"{}\")".format(service.decode("utf-8"), date_today()))
        conn.commit()

        conn.close()

    except Exception as err:
        print("[!] Error: {}".format(err))
        exit(1)

    # Ceate a sha512 string of the master password and the online service
    hash = hashlib.sha512()
    hash.update(prim_passw)
    prim_passw = hash.hexdigest()

    # Encode the created string to bytes to base64 encode it
    sec_passw = str.encode(prim_passw, "utf-8")
    encoded = base64.b64encode(sec_passw)

    # Display the first 20 chars of the string
    encoded_pw = encoded[:PASSW_LENGTH].decode("utf-8")
    print("Your password (hash, default):       {}".format(encoded_pw))

    # Display the last 20 chars of the string
    encoded_pw = encoded[-(PASSW_LENGTH+1):-1].decode("utf-8")
    print("Your password (hash, inverse):       {}".format(encoded_pw))

    chars = generate_extended_password(ALPHABET, prim_passw)
    print("Your password (alphabet):            {}".format("".join(chars)))

    # And one with extended
    chars = generate_extended_password(ALPHABET_EXTENDED, prim_passw)
    print("Your password (alphabet, extended):  {}".format("".join(chars)))

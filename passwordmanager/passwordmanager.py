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
import unittest

ALPHABET = ('abcdefghijklmnopqrstuvwxyzäöü'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'
            '0123456789!@#$%^&*()-_')
ALPHABET_EXTENDED = ('abcdefghijklmnopqrstuvwxyzäöü'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'
            '0123456789!"§$%&/()=?*+#.:,;-_')
PASSW_LENGTH = 20

class PWManager:
    def __init__(self):
        self.passw = "".encode("utf-8")
        self.passw_length = 20
        self.hash = hashlib.sha512()
        self.hash_digest = hashlib.sha512().hexdigest()
        self.encoded = base64.b64encode(b"")
        self.date = "1.1.2000"

    def __del__(self):
        pass

    def generate_password(self, password):
        self.post_password(password)
        self.create_sha_512_hash()
        self.base_64_encode()

    def post_password(self, password):
        self.passw = password.encode("utf-8")

    def create_sha_512_hash(self):
        # Ceate a sha512 string
        self.hash = hashlib.sha512()
        self.hash.update(self.passw)
        self.hash_digest = self.hash.hexdigest()

    def base_64_encode(self):
        # Encode the created string to bytes to base64 encode it
        temp = str.encode(self.hash_digest, "utf-8")
        self.encoded = base64.b64encode(temp)

    def get_passw_default(self):
        return self.encoded[:self.passw_length].decode("utf-8")

    def get_passw_default_inverse(self):
        return self.encoded[-(self.passw_length+1):-1].decode("utf-8")

    def get_passw_alphabet(self, alphabet):
        # Convert the hexdigest into decimal
        num = int(self.hash_digest, 16)

        num_chars = len(alphabet) # base to convert num
        chars = []

        # generate new password, one digit at a time up to password length
        while len(chars) < self.passw_length:
            num, index = divmod(num, num_chars)
            chars.append(alphabet[index])

        return "".join(chars)


def print_table_cmd_line(row):
    print("{0:3} | {1:20} | {2:10} | {3:10}".format(row[0], row[1], row[2], row[3]))

def date_today():
    now = datetime.datetime.now()
    date = str(now.day) + "." + str(now.month) + "." + str(now.year)

    return date

def display_db():
    try:
        # Open the db or create if not exists
        conn = sqlite3.connect("pwm.db") # pwm = passwordmanager

        # Show all services stored in db
        cursor = conn.execute("SELECT id, service, version, updated from SERVICES")

        print("[*] Existing services")
        print_table_cmd_line(["ID", "SERVICE", "VERSION", "UPDATED"])
        for row in cursor:
            print_table_cmd_line(row)

        conn.close()

    except Exception as err:
        print("[!] Error: {}".format(err))
        exit(1)

def get_version_of_service(service):
    try:
        # Open the db or create if not exists
        conn = sqlite3.connect("pwm.db") # pwm = passwordmanager

        # Show all services stored in db
        cursor = conn.execute("SELECT id, service, version, updated from SERVICES")

        # return corresponding version to service
        for row in cursor:
            if service == row[1]:
                return row[2]


        conn.close()
        return -1

    except Exception as err:
        print("[!] Error: {}".format(err))
        exit(1)

def get_service():
    print("Enter service name: ", end="")
    user_service = input().lower()

    return user_service

def get_master_passw_and_service():
    master_passw = getpass.getpass("[?] Enter master password     : ")
    print("[?] Enter the service to use  : ", end="")
    service = input()

    # If version greater than 1 add it to password to generate a new one
    version = get_version_of_service(service)
    if version > 1:
        return (master_passw + service + str(version))

    return (master_passw + service)

def get_master_passw_with_verification():
    master_passw_one = getpass.getpass("[?] Enter master password     : ")
    master_passw_two = getpass.getpass("[?] Verify master password    : ")
    if master_passw_one != master_passw_two:
        print("[!] Verification failed. Passwords are not equal.")
        return(-1)

    return master_passw_one

def add_new_password(master_passw, service):
    try:
        # Open the db or create if not exists
        conn = sqlite3.connect("pwm.db") # pwm = passwordmanager

        # create table if not exists
        conn.execute('''CREATE TABLE IF NOT EXISTS SERVICES
        (id INTEGER PRIMARY KEY,
        service TEXT NOT NULL,
        version INT DEFAULT 1,
        updated TEXT NOT NULL,
        UNIQUE(service));''')
        # service is the name of the service, version is a number so password can be changed without changing service name (to-do), created is a time string when it was last updated

        conn.execute("INSERT OR IGNORE INTO SERVICES (service, updated) VALUES(\"{}\", \"{}\")".format(service, date_today()))
        conn.commit()

        print("[*] New service added: {}".format(service))

        conn.close()

        return

    except Exception as err:
        print("[!] Error: {}".format(err))
        exit(1)

def change_password(master_passw, service):
    try:
        # Open the db or create if not exists
        conn = sqlite3.connect("pwm.db") # pwm = passwordmanager

        # Show all services stored in db
        cursor = conn.execute("SELECT id, service, version, updated from SERVICES")

        conn.execute("UPDATE SERVICES SET version = version + 1 WHERE service = \"{}\";".format(service))
        conn.commit()

        conn.close()

        return master_passw + service + str(get_version_of_service(service))

    except Exception as err:
        print("[!] Error: {}".format(err))
        exit(1)

def print_passwords():
    print("\n[*] Passwords")
    print("Your password (hash, default):       {}".format(pwm.get_passw_default()))
    print("Your password (hash, inverse):       {}".format(pwm.get_passw_default_inverse()))
    print("Your password (alphabet):            {}".format(pwm.get_passw_alphabet(ALPHABET)))
    print("Your password (alphabet, extended):  {}".format(pwm.get_passw_alphabet(ALPHABET_EXTENDED)))

def menu():
    print("\n[*] Menu")
    print("\t1: Generate existing password")
    print("\t2: Add new service to db")
    print("\t3: Change existing service in db")
    print("\t4: Exit")
    print("[?] Choose a number: ", end="")
    user_choosed = int(input())

    if user_choosed == 1:
        display_db()
        passw = get_master_passw_and_service()
        pwm.generate_password(passw)
        print_passwords()
    elif user_choosed == 2:
        master_passw = get_master_passw_with_verification()
        user_service = get_service()
        add_new_password(master_passw, user_service)
        pwm.generate_password(master_passw + user_service)
        print_passwords()
    elif user_choosed == 3:
        display_db()
        master_passw = get_master_passw_with_verification()
        user_service = get_service()
        change_password(master_passw, user_service)
        pwm.generate_password(master_passw + user_service + str(get_version_of_service(user_service)))
        print_passwords()
    elif user_choosed == 4:
        exit(0)
    else:
        print("[!] Error: Command not found")

if __name__ == "__main__":
    print("Welcome to PWManager.\nIt's a simple cmd line based password manager.")
    pwm = PWManager()
    menu()

    exit(0)

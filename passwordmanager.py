#!/usr/bin/env python3
'''
This little script is a simple password manager.
You give in your master password and the service you are using and based on this you get a some passwords.
'''
import hashlib
import base64
import getpass

ALPHABET = ('abcdefghijklmnopqrstuvwxyzäöü'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'
            '0123456789!@#$%^&*()-_')
ALPHABET_EXTENDED = ('abcdefghijklmnopqrstuvwxyzäöü'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'
            '0123456789!"§$%&/()=?*+#.:,;-_')
PASSW_LENGTH = 20

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
    # Ask for master password and used service
    master = getpass.getpass("Master password: ").encode("utf-8") # hides user input

    service = getpass.getpass("Login credentials: ").encode("utf-8").lower()
    prim_passw = master+service

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

passwordmanager
===============

It's a simple password manager. It needs two inputs. Your master password and a second one that should differ between each service, e.g. the service name. Then it creates four different passwords based on a SHA-512 hash.


# Install:
```bash
$ git clone https://github.com/thacoon/passwordmanager
$ cd passwormanager
```

# To user passwormanager.py:
```bash
$ python passwordmanager.py
```

# Example:
```bash
$ python passwordmanager.py
Master password:
Login credentials:
Your password (hash, default):       YmFmZDhjMmY2YTE3MmVl
Your password (hash, inverse):       xOGFmYzMxOTg2NmJkZTk
Your password (alphabet):            jJc%uRYtZvöb(gEkjm!$
Your password (alphabet, extended):  bpOgeäomk!%lOUbdü$gT
```

# To Do
Create a db to store service names, so just the master password needs to be remembered

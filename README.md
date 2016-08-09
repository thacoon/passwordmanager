passwordmanager
===============

It's a simple password manager. It needs two inputs. Your master password and a second one that should differ between each service, e.g. the service name. Then it creates four different passwords based on a SHA-512 hash. Then just copy and paste it into your login form.


# Install
```bash
$ git clone https://github.com/thacoon/passwordmanager
$ cd passwormanager
```

# Usage
```bash
$ python passwordmanager/passwordmanager.py
```

# Example
```bash
[shepard@core PasswordManagerGit]$ python passwordmanager/passwordmanager.py
Welcome to PWManager. It is a simple cmd line based password manager.

[*] Menu
	1: Generate existing password
	2: Add new service to db
	3: Change existing service in db
	4: Exit
[?] Choose a number: 1
[*] Existing services
ID  | SERVICE              | VERSION    | UPDATED   
  1 | github               |          2 | 9.8.2016  
[?] Enter master password     :
[?] Enter the service to use  : github

[*] Passwords
Your password (hash, default):       YzBlYWUxZjVmOGQ0YWI1
Your password (hash, inverse):       wOGEyNWQxZDVjMWRmM2I
Your password (alphabet):            ö&%2JNüWIü%ÜÜC^inj2ü
Your password (alphabet, extended):  l/Ä&WqTAVau/y0MSHG);
```

# Tests
```bash
$ python -m unittest
```


# To Do
* Change the versions in db, so password can be changed every x months

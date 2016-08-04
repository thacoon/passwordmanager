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
$ python passwordmanager.py
```

# Example
```bash
$ python passwordmanager.py
ID  | SERVICE              | VERSION    | UPDATED   
  1 | github               |          1 | 4.8.2016  
Master password:
Login credentials:
Your password (hash, default):       OWFmMDgxODkyMDEzZTEy
Your password (hash, inverse):       iODkxYzljZDg2MjIyMGQ
Your password (alphabet):            na8$EFQ6eY_HL5eJ8R$f
Your password (alphabet, extended):  Qmh*QHW.MHNZ(;äsR3M)

```

# To Do
* Change the versions in db, so password can be changed every x months

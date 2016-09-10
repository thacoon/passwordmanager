import unittest
from passwordmanager import passwordmanager as pwm


class TestFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ALPHABET = ('abcdefghijklmnopqrstuvwxyzäöü'
                         'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ'
                         '0123456789!@#$%^&*()-_')
        self.manager = pwm.PWGenerator()
        self.hash = ""
        self.encoding = ""

    @classmethod
    def tearDownClass(self):
        pass

    def test_01_post_password(self):
        self.manager.post_password("password")
        self.assertEqual(self.manager.passw, "password".encode("utf-8"))

    def test_02_create_sha_512_hash(self):
        hash_expected = "b109f3bbbc244eb82441917ed06d618b9008dd09b3befd1b5e07394c706a8bb980b1d7785e5976ec049b46df5f1326af5a2ea6d103fd07c95385ffab0cacbc86"  # hex digest of hash for "password", password is utf-8 encoded
        self.manager.create_sha_512_hash()

        self.assertEqual(hash_expected, self.manager.hash_digest)

    def test_03_base_64_encode(self):
        encoding_expected = b'YjEwOWYzYmJiYzI0NGViODI0NDE5MTdlZDA2ZDYxOGI5MDA4ZGQwOWIzYmVmZDFiNWUwNzM5NGM3MDZhOGJiOTgwYjFkNzc4NWU1OTc2ZWMwNDliNDZkZjVmMTMyNmFmNWEyZWE2ZDEwM2ZkMDdjOTUzODVmZmFiMGNhY2JjODY='
        self.manager.base_64_encode()

        self.assertEqual(encoding_expected, self.manager.encoded)

    def test_04_get_passw_default(self):
        passw_expected = "YjEwOWYzYmJiYzI0NGVi"
        passw = self.manager.get_passw_default()

        self.assertEqual(passw, passw_expected)
        self.assertEqual(len(passw), 20)

    def test_04_get_passw_default_inverse(self):
        passw_expected = "zODVmZmFiMGNhY2JjODY"
        passw = self.manager.get_passw_default_inverse()

        self.assertEqual(passw, passw_expected)
        self.assertEqual(len(passw), 20)

    def test_04_get_pass_alphabet(self):
        passw_expected = "JR-IXfüP-x#W&ulQaPö_"
        passw = self.manager.get_passw_alphabet(self.ALPHABET)

        self.assertEqual(passw, passw_expected)
        self.assertEqual(len(passw), 20)

    def test_05_generate_password(self):
        hash_digest_expected = "93f698c5ace36f9d68496b41d9b882ac565ac0f2d5f9decbdb34be9122155cd745398fa56ee5f9c6b353e78fc9cd1588e26a8ec97c355eed5f9f4e8cf707821b"
        encoding_expected = b"OTNmNjk4YzVhY2UzNmY5ZDY4NDk2YjQxZDliODgyYWM1NjVhYzBmMmQ1ZjlkZWNiZGIzNGJlOTEyMjE1NWNkNzQ1Mzk4ZmE1NmVlNWY5YzZiMzUzZTc4ZmM5Y2QxNTg4ZTI2YThlYzk3YzM1NWVlZDVmOWY0ZThjZjcwNzgyMWI="

        self.manager.generate_password("01234567")

        self.assertEqual(self.manager.hash_digest, hash_digest_expected)
        self.assertEqual(self.manager.encoded, encoding_expected)

if __name__ == "__main__":
    unittest.main()

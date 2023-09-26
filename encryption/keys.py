# -*- coding: utf-8 -*-
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Keys:

    def getMasterKey(self, mp, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(mp.encode())  # Can only use kdf once, type byte
        return key

    def getMasterCipher(self, key, iv):
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        return cipher

    def getCipher(self, pw, salt, iv):  #creates the cipher to encrypt and decrypt data based on given password
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
                )
        key = kdf.derive(pw.encode()) # Can only use kdf once, type byte
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        return cipher
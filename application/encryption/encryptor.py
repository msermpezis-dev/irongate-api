# -*- coding: utf-8 -*-
class Encryptor:

    def get_checkvalue(self, cipher):    #
        encryptor = cipher.encryptor()
        return encryptor.update(b"{xpz_^2LJ6[W8m]_") + encryptor.finalize() #can only encrypt bytes

    def get_mpcheckvalue(self, cipher):    #
        encryptor = cipher.encryptor()
        return encryptor.update(b"f.d4T*4cF-)2dFg/") + encryptor.finalize() #can only encrypt bytes

    def encrypt(self, text, cipher):
        if 16 < len(text) < 33:                                #if text given is more that 16bytes(=1 block)
            t1 = text[:16]                                                  #cuts the string into 2 parts of 16bytes
            t2 = text[16:]
            for i in range(0, 16-len(t2)):                                   #adds empty space to complete 16bytes
                t2 += " "
            encryptor = cipher.encryptor()
            v1 = encryptor.update(t1.encode()) + encryptor.finalize()       #makes string into bytes and then encrypts it
            encryptor = cipher.encryptor()
            v2 = encryptor.update(t2.encode()) + encryptor.finalize()
            value = v1 + v2
        else:
            for i in range(0, 16-len(text)):                                 #adds empty space to complete 16bytes
                text += " "
            encryptor = cipher.encryptor()
            value = encryptor.update(text.encode()) + encryptor.finalize()
        return value

    def encrypt_mk(self, key, cipher):
        t1 = key[:16]
        t2 = key[16:32]
        t3 = key[32:] + "    "
        encryptor = cipher.encryptor()
        v1 = encryptor.update(t1.encode()) + encryptor.finalize()  # makes string into bytes and then encrypts it
        encryptor = cipher.encryptor()
        v2 = encryptor.update(t2.encode()) + encryptor.finalize()
        encryptor = cipher.encryptor()
        v3 = encryptor.update(t3.encode()) + encryptor.finalize()
        value = v1 + v2 + v3
        return value
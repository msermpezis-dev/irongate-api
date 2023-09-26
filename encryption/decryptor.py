# -*- coding: utf-8 -*-
class Decryptor:

    def decrypt(self, text, cipher):
        if 16 < len(text) < 33:    #if text given is more that 16bytes(=1 block)
            decryptor = cipher.decryptor()                                  #then cuts the text to 2 parts and derypts
            di1 = decryptor.update(text[:16]) + decryptor.finalize()        #them seperately and afterwards combines them
            decryptor = cipher.decryptor()                                  #giving the full text(type bytes)
            di2 = decryptor.update(text[16:]) + decryptor.finalize()
            di = di1 + di2
        else:
            decryptor = cipher.decryptor()                                  #decrypts only 16bytes of string(type bytes)
            di = decryptor.update(text) + decryptor.finalize()
        return di

    def decrypt_mk(self, text, cipher):
        decryptor = cipher.decryptor()
        di1 = decryptor.update(text[:16]) + decryptor.finalize()
        decryptor = cipher.decryptor()
        di2 = decryptor.update(text[16:32]) + decryptor.finalize()
        decryptor = cipher.decryptor()
        di3 = decryptor.update(text[32:]) + decryptor.finalize()
        di = di1 + di2 + di3
        return di
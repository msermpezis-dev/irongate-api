# -*- coding: utf-8 -*-
import random
import os
import base64
from .wordlist import WordList


class Generator:

    def getNewSalt(self):
        return os.urandom(32)  # return 32 bytes

    def getNewIv(self):
        return os.urandom(16)  # return 16 bytes

    def getNewMnemonic(self):  # opens worldlist.txt, picks 12 random unique words and creates a sentence with them
        content = WordList().mp()
        phrase = ""
        c = 2047
        for i in range(12):
            n = random.randrange(0, c - i)
            phrase += content[n] + " "
            content.pop(n)
        return phrase[:-1]

    def stringToBinary(self, string):
        return base64.urlsafe_b64decode(string)

    def binaryToString(self, binary):
        return base64.urlsafe_b64encode(binary).decode('utf-8')



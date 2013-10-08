import nltk
import re

# hashtags dictionnary
class Hashtags:

    HT = {}
    def __init__(self):
        self.HT = {}


    def add(self, newHashtagName, newHashtag):
        if not self.has(newHashtagName):
            self.HT[newHashtagName] = []
        self.HT[newHashtagName].append(newHashtag)

    def has(self, hashtagName):
        return (hashtagName in self.HT)

    def get(self, hashtagName):
        return self.HT(hashtagName)



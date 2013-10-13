import csv

class Smileys:

    def __init__(self, path):
        self.SMILEYS_STRINGS = []
        self.SMILEYS_CATEGORIES = {}

        with open(path, "rb") as smileysFile:
            smileysReader = csv.reader(smileysFile, delimiter=',', quotechar='|')
            for row in smileysReader:
                self.SMILEYS_STRINGS.append(row[0])
                self.SMILEYS_CATEGORIES[row[0]] = row[1]

    def findSmileys(self, string):
        words = set(string.split())
        foundSmileys = filter(lambda x:x in self.SMILEYS_STRINGS, words)
        return foundSmileys

    def findEmotions(self, string):
        foundSmileys = self.findSmileys(string)
        matchingEmotions = map(lambda x: self.SMILEYS_CATEGORIES[x], foundSmileys)
        foundEmotions = list(set(matchingEmotions))
        return foundEmotions


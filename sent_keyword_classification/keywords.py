
import nltk
import re
import csv

# relevant keywords dictionnary
class Keywords:
    # handcrafted list of keyword names
    # names do not contain uppercase chars unless it's important
    KEYWORD_NAMES = []
    KEYWORD_CATEGORIES = {}
    with open("KEYWORDS.csv", "rb") as keywordsFile:
        keywordsReader = csv.reader(keywordsFile, delimiter=',', quotechar='|')
        for row in keywordsReader:
            KEYWORD_NAMES.append(row[0])
            KEYWORD_CATEGORIES[row[0]] = row[1]


    KW = {}
    def __init__(self):
        for kwName in self.KEYWORD_NAMES:
            # key: a keyword name
            # value: an array of postId containing that keyword
            self.KW[kwName] = [] 

    def listNames(self):
        return self.KEYWORD_NAMES 

    def listCategories(self):
        return self.KEYWORD_CATEGORIES

    def containsUppercaseChar(keywordName):                     # TODO: should be used to rank the keyword matching. 
        ucCharsList = re.findall(r"([A-Z])", keywordName)
        return len(ucCharsList) > 0

    def addOccurance(self, keywordName, keyword):
        self.KW[keywordName].append(keyword)


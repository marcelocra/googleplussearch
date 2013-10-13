#!/usr/bin/python

from LanguageCheck import Trigram
def test(): 
    line = "the text"
    unknown = Trigram(line)
    y = unknown.isEnglish()
    x = unknown.enSimilarity
    if y:
        print("input text is in English with similarity of " + str(x))
    else:
        print("input text is not in English with similarity of " + str(x))

if __name__ == '__main__':
    test()

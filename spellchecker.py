"""
spelling check based on Ethan Lib
date : 02 Oct 2013
author : J Samuel
"""
import json
import enchant
from enchant.tokenize import get_tokenizer

class spellCheck():
    def __init__(self):
        pass
    def spellcheck(self,text):
        d = enchant.Dict("en_US")
        tknzr = get_tokenizer("en_US")
        text2 = ""
        for (word,pos) in tknzr(text) :
            # checking slang word
            if d.check(word):
                text2 = text2 +" "+word
            else:
                print "err : ",word
                if self.checkslang(word) :
                    print "do nothing"
                else:
                    replword = d.suggest(word)
                    print replword[0]
                    text2 = text2 +" "+ replword[0]
        print text2
    def checkslang(self,text):
        return False

    def doCheck(self,jsonobj):
        decode = json.loads(jsonobj)
        for postobj in decode['posts']:
            pretext = postobj['post']['value']
            self.spellcheck(pretext)

            



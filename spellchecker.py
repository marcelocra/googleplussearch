# -*- coding: cp1252 -*-
"""
spelling check based on Ethan Lib
date : 02 Oct 2013
author : J Samuel

example :
>>> from wir_spellcheck import spellCheck
>>> t1 = spellCheck()
>>> t1.doCheck("{\"posts\":[{\"post\" :{\"value\":\"Languages are identigied by sfandard strng tags such as\"}},{\"post\" :{\"value\":\"A finer degree of control over the dibtionaries an how they are created can be ovtained using one or more\"}}]}")
err :  identigied
identified
err :  sfandard
standard
err :  strng
string
 Languages are identified by standard string tags such as
err :  dibtionaries
dictionaries
err :  ovtained
obtained
 A finer degree of control over the dictionaries an how they are created can be obtained using one or more
"""
import json
import enchant
import urllib
import re
from enchant.tokenize import get_tokenizer

re_wordFind = re.compile("[a-zA-Z0-9]+")

class spellCheck():
    def __init__(self):
        pass
    def spellcheck(self,text):
        d = enchant.Dict("en_US")
        words = re_wordFind.findall(text)
        text2 = ""
        for word in words :
            # checking slang word
            if d.check(word):
                text2 = text2 +" "+word
            else:
                if self.checkslang(word) == False :
                    replword = d.suggest(word)
                    if len(replword)>0:
                        text2 = text2 +" "+ replword[0]
                    else :
                        text2 = text2 +" "+word
                else :
                    text2 = text2+" "+word
        return text2
        
    def checkslang(self,text):
        url_info = urllib.urlopen('http://api.urbandictionary.com/v0/define?term='+text)
        result = ""
        for lines in url_info:
            result = result+lines
        decode = json.loads(result)
        if decode['result_type'] == 'no_results':
            return False
        else:
            return True

    def doCheck(self,jsonobj):
        decode = json.loads(jsonobj)
        for postobj in decode['posts']:
            pretext = postobj['post']['value']
            self.spellcheck(pretext)

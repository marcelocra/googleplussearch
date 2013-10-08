import nltk
from underscore import _
import re
import csv
from keywords import Keywords 
from hashtags import Hashtags 
from sent import SentiWordNetReader, SentiSynset
from smileys import Smileys


# init of hashtags & keywords dictionnaries
HASHTAGS = Hashtags()       # NOTE: global. The one & only instance of `class Hashtags`
KEYWORDS = Keywords()       # NOTE: global. The one & only instance of `class Keywords`
SENTIWORDNET = SentiWordNetReader("SENTIWORDNET.txt").all_senti_synsets()
SMILEYS = Smileys()         # NOTE: global. The one & only instance of `class Smileys`



class Post:
    def __init__(self, o):
        self.scanContent(o)
        self.scanMetadata(o)
        self.scanForHashtags()
        self.scanSmileys()
        self.detectRelevantKeywords()
        self.detectSent()
        print self.keywords

    def scanContent(self, o):
        self.content = nltk.util.clean_html(o["content"])
        self.tokens = nltk.tokenize.word_tokenize(self.content)
        #print self.content
        #print self.tokens

    def scanMetadata(self, o):
        self.id = o["postID"]
        #self.authorId = o["actor"]["id"]
        #self.authorName = o["actor"]["displayName"]

    def scanForHashtags(self):
        rawHashtags = re.findall(r"#([^ 0-9<>]+)", self.content)
        self.hashtags = map(lambda e:Hashtag(e, self.id), rawHashtags)

    def detectRelevantKeywords(self):
        relevantKeywordNames = filter(lambda e:e in KEYWORDS.listNames(), self.tokens)
        self.keywords = map(lambda e:Keyword(e, self.id), relevantKeywordNames)

    def detectSent(self):
        tokens = self.tokens
        #print SENTIWORDNET
        #for senti_synset in SENTIWORDNET:
            #print senti_synset.synset.name, senti_synset.pos_score, senti_synset.neg_score
            #print senti_synset 

    def scanSmileys(self):
        self.smileys = SMILEYS.findSmileys(self.content) 
        self.emotions = SMILEYS.findEmotions(self.content)
        print "####", self.emotions

    def getEmotions(self):
        return self.emotions

    def __repr__(self):
        return self.content + "//////" + self.hashtags

class Hashtag:
    def __init__(self, name, postId):
        self.name = name.lower()
        self.postId = postId
        HASHTAGS.add(self.name, self)

    def __repr__(self):
        return self.name + "/" + str(self.postId)

class Keyword:
    def __init__(self, name, postId):
        self.name = name.lower()
        self.nameCased = name
        self.postId = postId
        KEYWORDS.addOccurance(self.name, self)
    def __repr__(self):
        return self.name + "/" + KEYWORDS.listCategories()[self.name] + "/" + str(self.postId)


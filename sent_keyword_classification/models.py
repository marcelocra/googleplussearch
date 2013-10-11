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
SENTIWORDNET = SentiWordNetReader("SENTIWORDNET.txt")
SMILEYS = Smileys()         # NOTE: global. The one & only instance of `class Smileys`



class Post:
    def __init__(self, o):
        self.scanContent(o)
        self.scanMetadata(o)
        self.scanForHashtags(o)
        self.scanSmileys()
        self.detectRelevantKeywords()
        self.detectSent()
        print "# hashtags: ", self.hashtags
        print "# keywords: ", self.keywords
        print "# sentiments: ", self.emotions
        print "# content: ", self.content

    def scanContent(self, o):
        self.content = nltk.util.clean_html(o["content"])
        self.tokens = nltk.tokenize.word_tokenize(self.content)

    def scanMetadata(self, o):
        self.id = o["postID"]
        self.authorId = o["userID"]

    def scanForHashtags(self, o):
        self.hashtags = o['hashtags']
    
    def detectRelevantKeywords(self):
        relevantKeywordNames = filter(lambda e:e in KEYWORDS.listNames(), self.tokens)
        self.keywords = map(lambda e:Keyword(e, self.id), relevantKeywordNames)

    def detectSent(self):
        tokens = self.tokens
        #posList = map(lambda x : SENTIWORDNET.senti_synsets(x)[0].pos_score, tokens)
        p = q = o = []
        a = []
        scores = []
        for token in tokens:
            #synset = SENTIWORDNET.senti_synsets(token)
            scores.append(SENTIWORDNET.get_score(token))
            #if len(synset) > 0:
                ##print synset 
                #p.append(synset[0].pos_score)
                #q.append(synset[0].neg_score)
                #o.append(synset[0].obj_score)
                #s = str(synset[0].pos_score) + " " + str(synset[0].neg_score) + " " + str(synset[0].obj_score)
                #a.append(s)
            #print a
        if len(scores) > 0:
            output = sum(scores)/float(len(scores))
            print output
            return output
        #print p
        #print q
        #print o
        #for senti_synset in SENTIWORDNET:
            #print senti_synset.synset.name, senti_synset.pos_score, senti_synset.neg_score
            #print senti_synset 

    def scanSmileys(self):
        self.smileys = SMILEYS.findSmileys(self.content) 
        self.emotions = SMILEYS.findEmotions(self.content)

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
        return self.name + "/" + KEYWORDS.listCategories()[self.name] #+ "/" + str(self.postId)


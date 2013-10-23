import json
import codecs
import nltk
import os.path
import pickle
from nltk.corpus import stopwords
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

WORDS = {}
ALL_WORDS = []
    

        

def word_feats(words):
    return dict([(word, True) for word in words])

class Post:
    def __init__(self, content, isPositive):
        self.content = content
        self.isPositive = isPositive
   
        self.tagWords()


    def getWords(self):
        filteredWords = filter(lambda w :  not w in stopwords.words("english"), self.words)
        return filteredWords

    def tagWords(self):
        self.words = map(lambda w : w.lower(), nltk.tokenize.word_tokenize(self.content))
        ALL_WORDS.extend(self.words)
        for word in self.words:
            WORDS[word] = self.isPositive

    def __repr__(self):
        return self.content + "/" + str(self.isPositive)

if os.path.exists("save.p"):
    classifier = pickle.load( open( "save.p", "rb" ) )

else:
    # analyze posts 
    p = open("pos.txt", "r")
    posPosts = p.readlines()
    n = open("neg.txt", "r")
    negPosts = n.readlines()


    NEG_POSTS =  map(lambda post : Post(post, False), negPosts)
    POS_POSTS = map(lambda post : Post(post, True), posPosts)
    TAGGED_POSTS = NEG_POSTS + POS_POSTS

    negfeats = [(word_feats(post.getWords()), 'neg') for post in NEG_POSTS]
    posfeats = [(word_feats(post.getWords()), 'pos') for post in POS_POSTS]

    trainfeats = negfeats + posfeats
    classifier = NaiveBayesClassifier.train(trainfeats)
    print 'reginerating...'
    pickle.dump(classifier, open("save.p", "wb"))
#for testfeat in testfeats:
    #print('{s} => {c}'.format(s = testfeat, c = classifier.classify(testfeat)))


#outputfiles = [ "output_audi_posts.txt", "output_bmw_posts.txt", "output_driving_posts.txt", "output_imdb_posts.txt", "output_iphone_posts.txt", "output_music_posts.txt", "output_posts.txt", "output_racing_posts.txt", "output_randomposts.txt", "output_technology_posts.txt", "output_television_posts.txt"]

outputfiles = ["output_audi_posts.txt", "output_bmw_posts.txt", "output_driving_posts.txt", "output_imdb_posts.txt", "output_iphone_posts.txt", "output_microsoft_posts.txt", "output_music_posts.txt", "output_posts.txt", "output_racing_posts.txt", "output_randomposts.txt", "output_sony_posts.txt", "output_technology_posts.txt", "output_television_posts.txt"]


for f in outputfiles:
    print "processing file ", f
    t = codecs.open("outputs/" + f, "r", "utf-8")
    testPosts = t.readlines()

    newf = "new_" + f
    n = codecs.open("new_outputs/" + f, "a+", "utf-8")
    newPosts = n.readlines()

    for line in testPosts:
        jsonline = json.loads(line)
        test = jsonline["cleanContent"]
        post = Post(test, True)
        feat = word_feats(post.getWords())
        classif = classifier.classify(feat)
        jsonline["sentiment_polarity"] = classif
        newline = json.dumps(jsonline)
        try:
            #print('{s} => {c}'.format(s = post.content, c = classif))
            n.write(newline + '\r\n')
        except UnicodeEncodeError:
            pass
    n.close()
    t.close()

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


t = open("testneg.csv", "r")
testPosts = t.readlines()
TEST_POSTS = map(lambda post : Post(post, True), testPosts)
testfeats = [word_feats(post.getWords()) for post in TEST_POSTS]
wrongs = 0
for test in testPosts:
    post = Post(test, True)
    feat = word_feats(post.getWords())
    classif = classifier.classify(feat)
    if classif != "neg":
        wrongs = wrongs + 1
    print('{s} => {c}'.format(s = post.content, c = classif))
print "wrongs: ", wrongs, " over ", len(testPosts)
print "error rate: ", float(wrongs)/len(testPosts)




#print TAGGED_POSTS
#print WORDS
#print ALL_WORDS

## order by frequency
#wordfreq = nltk.FreqDist(ALL_WORDS)
#ORDERED_WORDS = wordfreq.keys()
#print ORDERED_WORDS 

#FILTERED_ORDERED_WORDS = filter(lambda w :  not w in stopwords.words("english"), ORDERED_WORDS)

#print FILTERED_ORDERED_WORDS

#def feature_extractor(doc):
#    docwords = set(doc)
#    features = {}
#    for i in FILTERED_ORDERED_WORDS:
#        features['contains(%s)' % i] = (i in docwords)
#    return features 

#training_set = nltk.classify.apply_features(feature_extractor, TAGGED_POSTS)
#classifier = nltk.NaiveBayesClassifier.train(training_set)

#print classifier.show_most_informative_features(n=30)



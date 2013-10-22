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
        filteredWords = self.words 
        return filteredWords

    def tagWords(self):
        self.words = map(lambda w : w.lower(), nltk.tokenize.word_tokenize(self.content))
        ALL_WORDS.extend(self.words)
        for word in self.words:
            WORDS[word] = self.isPositive

    def __repr__(self):
        return self.content + "/" + str(self.isPositive)

# analyze posts 
p = open("pos.txt", "r")
posPosts = p.readlines()
n = open("neg.txt", "r")
negPosts = n.readlines()


NEG_POSTS =  map(lambda post : Post(post, False), negPosts)
POS_POSTS = map(lambda post : Post(post, True), posPosts)
TAGGED_POSTS = NEG_POSTS + POS_POSTS

#### TEST POSTS
ratio = .8
limit_index = int(.8 * len(NEG_POSTS))
TEST_NEG_POSTS = NEG_POSTS[limit_index:]
NEG_POSTS = NEG_POSTS[:limit_index]

limit_index = int(.8 * len(POS_POSTS))
TEST_POS_POSTS = POS_POSTS[limit_index:]
POS_POSTS = POS_POSTS[:limit_index]
####
if os.path.exists("save.p"):
    classifier = pickle.load( open( "save.p", "rb" ) )

else:
    print 'reginerating...'

    negfeats = [(word_feats(post.getWords()), 'neg') for post in NEG_POSTS]
    posfeats = [(word_feats(post.getWords()), 'pos') for post in POS_POSTS]

    trainfeats = negfeats + posfeats
    classifier = NaiveBayesClassifier.train(trainfeats)
    pickle.dump(classifier, open("save.p", "wb"))
#for testfeat in testfeats:
    #print('{s} => {c}'.format(s = testfeat, c = classifier.classify(testfeat)))

print "\n testing positives"
testfeats = [word_feats(post.getWords()) for post in TEST_POS_POSTS]

falseNeg = 0
truePos = 0
trueNeg = 0
total = 0

wrongs = 0
rights = 0
nb_positives_retrieved = 0
nb_positives_actual = 0
nb_negatives_retrieved = 0
nb_negatives_actual = 0
for test in TEST_POS_POSTS:
    post = test
    feat = word_feats(post.getWords())
    classif = classifier.classify(feat)
    if classif == "neg":
        wrongs = wrongs + 1
        nb_negatives_retrieved +=1
    else:
        rights += 1
        nb_positives_retrieved += 1
    #print('{s} => {c}'.format(s = post.content, c = classif))
nb_positives_actual = len(TEST_POS_POSTS)
print "wrongs: ", wrongs, " over ", len(TEST_POS_POSTS)
print "error rate: ", float(wrongs)/len(TEST_POS_POSTS)

falseNeg += wrongs 
truePos += rights
total += len(TEST_POS_POSTS)

print "\ntesting negatives"
testfeats = [word_feats(post.getWords()) for post in TEST_NEG_POSTS]
wrongs = 0
rights = 0
for test in TEST_NEG_POSTS:
    post = test
    feat = word_feats(post.getWords())
    classif = classifier.classify(feat)
    if classif == "pos":
        wrongs = wrongs + 1
        nb_positives_retrieved += 1
    else:
        nb_negatives_retrieved +=1
        rights += 1
    #print('{s} => {c}'.format(s = post.content, c = classif))
print "wrongs: ", wrongs, " over ", len(TEST_NEG_POSTS)
print "error rate: ", float(wrongs)/len(TEST_NEG_POSTS)
nb_negatives_actual = len(TEST_NEG_POSTS)
trueNeg += rights 

falseNeg += wrongs 
total += len(TEST_NEG_POSTS)

#print "falseNeg ", falseNeg, falseNeg/float(total)
#print "truePos ", truePos, truePos/float(total)
print "test set ", total, " posts"
print "\nfor positive posts"
#print "precision ", nb_positives_retrieved/float(nb_positives_actual)
print "precision ", truePos/float(nb_positives_retrieved)
print "recall ", truePos/float(nb_positives_actual)
print "\nfor negative posts"
print "precision ", trueNeg/float(nb_negatives_retrieved)
print "recall ", trueNeg/float(nb_negatives_actual)

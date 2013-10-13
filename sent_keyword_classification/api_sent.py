
from sent import SentiWordNetReader, SentiSynset
from smileys import Smileys


SWN = SentiWordNetReader("SENTIWORDNET.txt")
SMILEYS = Smileys("SMILEYS.csv")



text = "I am very angry to see this not working :("
sent_score = SWN.get_sentiment(text)
sent_emotions = SMILEYS.findEmotions(text)
clean_string = SMILEYS.removeSmileys(text)

print "sentiment score (pos/neg/obj):", sent_score 
print "sentiment emotions (smileys):", sent_emotions
print "clean string ", clean_string





from underscore import _
import codecs
from collections import namedtuple
import json
from pprint import pprint
##
from models import Post, HASHTAGS, KEYWORDS
import dao




# fetching the posts
#with codecs.open("data.json", "r", "utf-8") as data_file:
    #data = json.load(data_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    #posts = data.items

#dao.buildPosts(posts)
with codecs.open("output.txt", "r", "utf-8") as data_file:
    lines = data_file.readlines()
    data_file.close()
    posts = map(lambda x: json.loads(x), lines)

dao.buildPosts(posts)

#print HASHTAGS.HT
#print HASHTAGS.HT['kde'][0]
#print "*********************"
#print KEYWORDS.KW

#for post in posts:
    #print json.dumps(post.object.content, sort_keys=True, indent=4, separators=(',', ': '))

# fetching dict
#with open("sentiwordnet.csv") as dict_file:
    #reader = csv.reader(f)
    #for row in reader:
        #print ', '.join(row)

#swn = SentiWordNetReader("SENTIWORDNET.txt")
#for senti_synset in swn.all_senti_synsets():
    #print senti_synset.synset.name, senti_synset.pos_score, senti_synset.neg_score



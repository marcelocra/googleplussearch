from underscore import _
import codecs
import re
#from nltk.corpus import wordnet as wn
try:
    from nltk.corpus import wordnet as wn
except ImportError:
    sys.stderr.write("Couldn't find an NLTK installation. To get it: http://www.nltk.org/.\n")
    sys.exit(2)

class SentiWordNetReader:
    def __init__(self, filename):
        self.filename = filename
        self.db = {}
        self.parse()

    def parse(self):
        lines = codecs.open(self.filename, "r", "utf-8").read().splitlines()
        # excluding comments
        lines = filter((lambda x : not re.search(r"^\s*#", x)), lines) 
        for i, line in enumerate(lines):
            fields = re.split(r"\t+", line)
            fields = map(unicode.strip, fields)
            try:
                pos, offset, pos_score, neg_score, synset_terms, gloss = fields
            except:
                sys.stderr.write("Line %s formatted incorrectly: %s\n" % (i, line))
            if pos and offset:
                offset = int(offset)
                self.db[(pos, offset)] = (float(pos_score), float(neg_score))

    def senti_synset(self, *vals):
        if tuple(vals) in self.db:
            pos_score, neg_score = self.db[tuple(vals)]
            pos, offset = vals
            synset = wn._synset_from_pos_and_offset(pos, offset)
            return SentiSynset(pos_score, neg_score, synset)
        else:
            synset = wn.synset(vals[0])
            pos = synset.pos
            offset = synset.offset
            if (pos, offset) in self.db:
                pos_score, neg_score = self.db[(pos, offset)]
                return SentiSynset(pos_score, neg_score, synset)
            else:
                return None

    def senti_synsets(self, string, pos=None):
        sentis = []
        synset_list = wn.synsets(string, pos)
        for synset in synset_list:
            sentis.append(self.senti_synset(synset.name))
        sentis = filter(lambda x : x, sentis)
        return sentis

    def all_senti_synsets(self):
        for key, fields in self.db.iteritems():
            pos, offset = key
            pos_score, neg_score = fields
            synset = wn._synset_from_pos_and_offset(pos, offset)
            yield SentiSynset(pos_score, neg_score, synset)

class SentiSynset:
    def __init__(self, pos_score, neg_score, synset):
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.obj_score = 1.0 - (self.pos_score + self.neg_score)
        self.synset = synset
    def __repr__(self):
        return "senti" + repr(self.synset)




#swn = SentiWordNetReader("SENTIWORDNET.txt")
#for senti_synset in swn.all_senti_synsets():
    #print senti_synset.synset.name, senti_synset.pos_score, senti_synset.neg_score


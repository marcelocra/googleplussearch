# coding: utf-8


class Synonyms(object):
    def __init__(self, word, synonyms=None):
        self.word = word
        if synonyms is None:
            synonyms = []
        self.synonyms = synonyms
        self.offset = 0

    def next_meaning(self):
        self.offset += 1
        if self.offset >= len(self.synonyms):
            self.offset = 0
        return self.synonyms[self.offset]

    def words(self):
        return self.synonyms[self.offset].lemma_names

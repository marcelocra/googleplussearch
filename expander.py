# coding: utf-8


import nltk
from nltk.corpus import wordnet
from synonyms import Synonyms


class Expander(object):
    """
    Receive a list with all English words that
    the user typed in the query. If the user provides the query during the 
    creation of the object, she can access the expanded query using the
    variable 'expanded_query'. Otherwise it is necessary to call all the
    methods to create the expanded query, as follows:

    Ex.:
        >>> query = ['how', 'to', 'use', 'a', 'hammer']
        >>> query_without_stopwords = expander.remove_stopwords(query)
        >>> synonyms_list = expander.create_synonyms_list(query_without_stopwords)
        >>> expanded_query = expander.expand_query(synonyms_list)
        >>> expanded_query
        ['use', 'usage', 'utilization', 'utilisation', 'employment', 'exercise', 'hammer', 'cock']\

    """
    def __init__(self, query=None):
        if query is not None:
            self.original_query = query
            self.query_without_stopwords = self.remove_stopwords(query)
            self.synonyms_list = self.create_synonyms_list(self.query_without_stopwords)
            self.expanded_query = self.expand_query(self.synonyms_list)

    def remove_stopwords(self, query):
        stopwords = nltk.corpus.stopwords.words('english')
        query_without_stopwords = []
        for word in query:
            if word not in stopwords:
                query_without_stopwords.append(word)
        return query_without_stopwords

    def create_synonyms_list(self, query_without_stopwords):
        synonyms_list = {}
        for word in query_without_stopwords:
            try:
                synonyms = Synonyms(word, wordnet.synsets(word))
                synonyms_list[word] = synonyms
            except:
                print "The was a problem processing the following word:", word
        return synonyms_list

    def expand_query(self, synonyms_list):
        expanded_query = []
        for synonyms in synonyms_list.values():
            expanded_query.extend(synonyms.words())
        return expanded_query


if __name__ == '__main__':
    expander = Expander()
    query = ['how', 'to', 'use', 'a', 'hammer']
    query_without_stopwords = expander.remove_stopwords(query)
    synonyms_list = expander.create_synonyms_list(query_without_stopwords)
    expanded_query = expander.expand_query(synonyms_list)
    print expanded_query

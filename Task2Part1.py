from __future__ import print_function
import pysolr

import sys
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer

# Splits the corpus into articles. Further splits each article into sentences and tokenizes each sentence.
# The words in each sentence is stored as a vector of its words and is indexed using solr
#
# Authors: Nanditha Valsaraj, Shreya Vishwanath Rao, Ramya Elangovan
# Version 1.0: 12/5/2017

if(sys.argv):
    datafile=open(sys.argv[1], 'r');

text =datafile.read()

# Setup a Solr instance.
solr = pysolr.Solr('http://localhost:8983/solr/news', timeout=10)

#split to articles
a=text.split('\n\n')
for i in range(0,len(a)):

    #split into sentences
    lemma = []
    c = []
    stem = []
    b = []

    sent_all = sent_tokenize(a[i])
    words = WordPunctTokenizer()
    lmtzr = WordNetLemmatizer()
    porter_stemmer = PorterStemmer()
    for j in range(0,len(sent_all)):
        wrds=words.tokenize(sent_all[j])
        for k in (wrds):
            c.append(lmtzr.lemmatize(k))
            b.append(porter_stemmer.stem(k))
        lemma.append(c);
        stem.append(b);
        c=[]
        b = []

    #loading data into solr
    for j in range(0,len(sent_all)):
        id="A"+str(i)+" S"+str(j);
        solr.add([{"id":id,"content":words.tokenize(sent_all[j]),"POS_TAG":nltk.pos_tag(words.tokenize(sent_all[j])),"LEMMA":lemma[j],"STEM":stem[j]}])



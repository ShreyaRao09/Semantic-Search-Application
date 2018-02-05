from __future__ import print_function
import pysolr
from nltk.parse import stanford
import sys
import nltk
import os

nltk.internals.config_java("C:/Program Files (x86)/Java/jdk1.7.0_55/bin/java.exe")
from nltk.tokenize import sent_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.wsd import lesk

os.environ['CLASSPATH'] = 'C:/stanford-corenlp-full-2017-06-09'
os.environ['STANFORD_PARSER'] = 'C:/stanford-parser-full-2014-08-27'
os.environ['STANFORD_MODELS'] = 'C:/stanford-parser-full-2014-08-27'

path_to_model = "C:/stanf" \
                "ord-english-corenlp-2017-06-09-models.jar"
path_to_jar = "C:/stanford-parser-full-2014-08-27/stanford-parser.jar"

# Splits the corpus into articles. Further splits each article into sentences and tokenizes each sentence.
# The words in each sentence is stored as a vector of its words,pos tags, lemmas, stems, hypernyms, hyponyms,
# meronyms, holonyms, dependency parse relations and is indexed using solr
#
# Authors: Nanditha Valsaraj, Shreya Vishwanath Rao, Ramya Elangovan
# Version 1.0: 12/5/2017

if (sys.argv):
    datafile = open(sys.argv[1], 'r');

text = datafile.read()

# Setup a Solr instance.
solr = pysolr.Solr('http://localhost:8983/solr/Task3', timeout=100)

# split to articles
a = text.split('\n\n')

for i in range(0, len(a)):

    lemma = []
    c = []
    stem = []
    b = []
    hyper = []
    hypernyms = []
    hypo = []
    hyponyms = []
    mero = []
    meronyms = []
    holo = []
    holonyms = []
    NP = []
    phrases = []
    depList = []
    id = []

    # split into sentences
    sent_all = sent_tokenize(a[i])

    words = WordPunctTokenizer()
    lmtzr = WordNetLemmatizer()
    porter_stemmer = PorterStemmer()

    for j in range(0, len(sent_all)):
        name = "A" + str(i) + " S" + str(j);
        id.append(name);
        wrds = words.tokenize(sent_all[j])
        for k in (wrds):
            c.append(lmtzr.lemmatize(k))
            b.append(porter_stemmer.stem(k))
            bestSynonym = lesk(wrds, k)
            if bestSynonym is not None:
                for hypernym in bestSynonym.hypernyms()[:2]:
                    hyper.append(hypernym)
                for hyponym in bestSynonym.hyponyms()[:2]:
                    hypo.append(hyponym)
                for meronym in bestSynonym.part_meronyms()[:2]:
                    mero.append(meronym)
                for holonym in bestSynonym.part_holonyms()[:2]:
                    holo.append(holonym)

        lemma.append(c);
        stem.append(b);
        hypernyms.append(hyper);
        hyponyms.append(hypo);
        meronyms.append(mero);
        holonyms.append(holo);
        c = []
        b = []
        hyper = []
        hypo = []
        mero = []
        holo = []

    for j in range(0, len(sent_all)):
        depparser = stanford.StanfordDependencyParser(path_to_model, path_to_jar)
        result = depparser.raw_parse(sent_all[j])
        newResult = result.__next__()
        # for triple in dep.triples():
        #     print (triple)
        dep = list(newResult.triples())
        depList.append(dep)

    #adding content to solr
    for j in range(0, len(sent_all)):
        solr.add(
            [{"ID": id[j], "CONTENT": words.tokenize(sent_all[j]), "POS_TAG": nltk.pos_tag(words.tokenize(sent_all[j])),
              "LEMMA": lemma[j], "STEM": stem[j], "HYPERNYM": hypernyms[j], "HYPONYM": hyponyms[j],
              "MERONYMS": meronyms[j],
              "HOLONYMS": holonyms[j], "DEPENDENCYPARSE": depList[j]}])



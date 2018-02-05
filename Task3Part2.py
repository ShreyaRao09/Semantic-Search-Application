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

path_to_model = "C:/stanford-english-corenlp-2017-06-09-models.jar"
path_to_jar = "C:/stanford-parser-full-2014-08-27/stanford-parser.jar"

# Splits the corpus into articles. Further splits each article into sentences and tokenizes each sentence.
# The words in each sentence is added to a query string of its words,pos tags, lemmas, stems, hypernyms, hyponyms,
# meronyms, holonyms, dependency parse relations and is then used to extract the sentences
# that correspond to it using solr
#
# Authors: Shreya Vishwanath Rao, Nanditha Valsaraj, Ramya Elangovan
# Version 1.0: 12/5/2017

if (sys.argv):
    stringData = open(sys.argv[2], 'r');
    datafile = open(sys.argv[1], 'r');

corpus = datafile.read()
text=stringData.read()

# Setup a Solr instance.
solr = pysolr.Solr('http://localhost:8983/solr/Task3', timeout=100)


a = text.split('\n\n')
corp=corpus.split('\n\n')

words = WordPunctTokenizer()
lmtzr = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
searchdata=""

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

    for j in range(0, len(sent_all)):
        depparser = stanford.StanfordDependencyParser(path_to_model, path_to_jar)
        result = depparser.raw_parse(sent_all[j])
        newResult = result.__next__()
        dep = list(newResult.triples())
        depList.append(dep)

    inputsentlen = len(sent_all)

    for j in range(0, inputsentlen):

        wrdsData=words.tokenize(sent_all[j])
        for k in range(0,len(wrdsData)):
            searchdata += "CONTENT:" + "".join(wrdsData[k]) + " & "

        posData= nltk.pos_tag(words.tokenize(sent_all[j]))
        for k in range(0, len(posData)):
            searchdata += "POS_TAG:" + "("+"".join(posData[k][0])+ ", " + "".join(posData[k][1]) + ") & "

        lemmaData = lemma[j]
        for k in range(0, len(lemmaData)):
            searchdata += "LEMMA:" + "".join(lemmaData[k]) + " & "

        stemData = stem[j];
        for k in range(0, len(stemData)):
            searchdata += "STEM:" + "".join(stemData[k]) + " & "

        hyperData = hypernyms[j]
        for k in range(0, len(hyperData)):
            # print(hyperData[k])
            searchdata += "HYPERNYM:" +str(hyperData[k]) + " & "

        hypoData = hyponyms[j]
        for k in range(0, len(hypoData)):
            searchdata += "HYPONYM:" + str(hypoData[k]) + " & "

        meroData = meronyms[j]
        for k in range(0, len(meroData)):
            searchdata += "MERONYMS:" + str(meroData[k]) + " & "

        holoData = holonyms[j]
        for k in range(0, len(holoData)):
            searchdata += "HOLONYMS:" + str(holoData[k]) + " & "

        depData = depList[j]
        depLen=len(depList)
        for k in range(0, len(depData)):
            if (k != (depLen - 1)) or (i != len(sent_all) - 1):
                searchdata += "DEPENDENCYPARSE:" + str(depData[k]) + " & "
            else:
                searchdata += "DEPENDENCYPARSE:" + str(depData[k])

print("\nQuery String:")
print(searchdata)
print("\nSentence matches are:")
results = solr.search(q=searchdata);

# Just loop over it to access the results.
for result in results:
    ans=result['ID']
    idVal=str(ans[0])
    parts=words.tokenize(idVal)
    article=parts[0][1:]
    sentence=parts[1][1:]
    print("ID:'{0}'".format(idVal))
    sent_all = sent_tokenize(corp[int(article)])
    print(sent_all[int(sentence)])
    print()


from __future__ import print_function
import pysolr

import sys

from nltk.tokenize import sent_tokenize
from nltk.tokenize import WordPunctTokenizer

# Splits the input content into sentences and further tokenizes each sentence.
# The words in each sentence is added to a query string of its words and is then used to extract the sentences
# that correspond to it using solr
#
# Authors: Nanditha Valsaraj, Shreya Vishwanath Rao, Ramya Elangovan
# Version 1.0: 12/5/2017

if(sys.argv):
    stringData=open(sys.argv[2], 'r');
    datafile=open(sys.argv[1], 'r');

#read the corpus
text =datafile.read()
inputsent=stringData.read();

a=text.split('\n\n')

# Setup a Solr instance.
solr = pysolr.Solr('http://localhost:8983/solr/Task2', timeout=10)
inputsent_all=sent_tokenize(inputsent)
inputwords=WordPunctTokenizer()
searchdata=""
for i in range(0,len(inputsent_all)):

    inputwordslist=inputwords.tokenize(inputsent_all[i])
    inputsentlen=len(inputwordslist)

    for j in range(0,inputsentlen):
        if(j!=(inputsentlen-1)) or (i!=len(inputsent_all)-1):
            searchdata+="content:"+"".join(inputwordslist[j])+" & "
        else:
            searchdata+="content:"+"".join(inputwordslist[j])

print("\nQuery String:")
print (searchdata)
print("\nSentence matches are:")
results = solr.search(q=searchdata);
# Just loop over it to access the results.
for result in results:
    ans=result['id']
    parts=inputwords.tokenize(ans)
    article=parts[0][1:]
    sentence=parts[1][1:]
    print("ID:'{0}'".format(ans))
    sent_all = sent_tokenize(a[int(article)])
    print(sent_all[int(sentence)])
    print()



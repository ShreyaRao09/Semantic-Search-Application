from __future__ import print_function
import pysolr
from nltk.parse import stanford
import sys
import nltk
import glob
import os

from nltk.tokenize import sent_tokenize
from nltk.tokenize import WordPunctTokenizer
import string

# Counts the number of words in the corpus
#
# Authors: Shreya Vishwanath Rao, Nanditha Valsaraj, Ramya Elangovan
# Version 1.0: 12/5/2017

if(sys.argv):
    datafile=open(sys.argv[1], 'r');

text =datafile.read()

#split to articles
a=text.split('\n\n')
count=0
for i in range(0,len(a)):

    #split into sentences
    sent_all = sent_tokenize(a[i])

    words = WordPunctTokenizer()

    for j in range(0, len(sent_all)):
        wrds = words.tokenize(sent_all[j])
        for k in (wrds):
            if k in string.punctuation:
                continue
            count = count + 1

print(count)


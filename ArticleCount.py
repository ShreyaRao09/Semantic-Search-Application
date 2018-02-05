from __future__ import print_function
import sys

# Counts the number of articles in the corpus
#
# Authors: Shreya Vishwanath Rao, Nanditha Valsaraj, Ramya Elangovan
# Version 1.0: 12/5/2017


if(sys.argv):
    datafile=open(sys.argv[1], 'r');

text =datafile.read()
a=text.split('\n\n')
count=0
for i in range(0,len(a)):
    count=count+1
print(count)


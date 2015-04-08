# -*- coding: utf-8 -*-
"""
John Hewitt
2/15/15
Writing a PMI to pass through text files
    -open file --done
    -need to get w1, w2 --done
    -import stop-words filter. remove all occurrences of words that are in this set before we work more intensively with the calculations
    -find 
        --gram[] ; list of sample words, by window n -done
        --tot ; all words in sample space --word count, done
    -look for index of words and count occurrences (Collection.counter(set)) -done
    -apply PMI -done
        --rinse, repeat PMI for all sets of words in text
    -print results
    -find a good threshold to return meaningful word pairs
    -apply threshold to filter out poor results
    -always close resources
"""

import math
from collections import Counter
from sys import argv
import re

punct = re.compile(r'[!?,:;/()]')
#functions used by PMI application from line 24 - 64
#Dr Francisco Iacobelli provided the PMI and N-grams functions
def pmi(w1, w2, grams, tot):
    return math.log((grams[w1 + " " + w2] * 1.0) / (grams[w1] * grams[w2]) * tot)

def ngrams(input, n):
    input = input.split(" ")
    output = []
    for i in range(len(input)- n + 1):
        output.append(" ".join(input [i:i+n]))
    return output

#open and split file
def file2list(filename):
    text = open(filename).read()
    return normalize_words(text.replace("\n"," ").split(" "))
    

def normalize_words(word_list):
    l = [replace_punct(x).lower() for x in word_list]
    return [x for x in l if len(l)>0]

def replace_punct(x):
    return punct.sub("",x).replace(".","").strip()

def wordCounter(l_words):
    return Counter(l_words)

#nested for loop goes through a string to retrieve all possible word pair combinations
def bigramCombination(listString):
    newList = []
    for i,e1 in enumerate(listString[:-1]):
        for e2 in listString[i+1:]:
            newItem = e1 + " " + e2
            newList.append(newItem.lower())
    return newList
        
#window shifter, gets first window, moves position by one, appends all combinations to the last element
def windowShift(listString, initialN):
    newList = bigramCombination(listString[:initialN])
    #first window
    for i in range(1,len(listString)-initialN+1):
        for e1 in listString[i:i+initialN-1]:
            #print e1,i,i+initialN-1,initialN+1
            newItem1 = e1 + " " + listString[initialN+i-1]
            newList.append(newItem1.lower())
    return newList
        
def printHeader():
    return "Word\tCount\n"

#!!tab spacing is not consistent with string length!!
#so the tab may be there in the code / formatting but it will not appear so
def wordListPrinter(testList, testFile):
    for key,val in testList.items():
        if len(key)>0:
            testFile.write("%s\t%s\n" % (key, val))

def process_file(filename,window_size):
    listString = file2list(filename)
    listWindow = windowShift(listString, window_size)
    counted_unigrams = wordCounter(listString)
    counted_bigrams = wordCounter(listWindow)
    total_words = len(listString)
    counted_unigrams["@#total#@"]=total_words
    counted_unigrams.update(counted_bigrams)
    return counted_unigrams


def write_counter(outfilename,counter):
    testFile = open(outfilename, "w")
    #testFile.write(printHeader())
    wordListPrinter(counter, testFile)
    

if __name__=='__main__':
    script, filename, outfilename = argv
    counts = process_file(filename,5)
    write_counter(outfilename,counts)

"""
excess test code
#return counted list
wordListCounted = wordCounter(wordList1)

#get bigrams
wordListGrams = ngrams(open(fileName).read(), 2)

#bigram pair counts for PMI
wordListGramsCounted = wordCounter(wordListGrams)

#gram collections for pmi
wordListAndGrams = wordListCounted + wordListGramsCounted

#bigramList = bigramCombination(wordList1)

#print (bigramList)
#print pmi("of", "Shiloh,", wordListAndGrams, 278)
#print wordListAndGrams
#open test file, and split it into words
#fileName = "shiloh.txt"
#fileFolder = [] #will implement later for multiple document analysis
#wordList1 = file2list(fileName)
#print wordWindows
#wordWindows = windowShift(wordList1, 4)
"""

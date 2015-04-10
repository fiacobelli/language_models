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
import cPickle
import os, fnmatch,datetime
from pprint import pprint

punct = re.compile(r'\W')
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


def locate(pattern, root_path):
    for path, dirs, files in os.walk(os.path.abspath(root_path)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)


def process_folder(folder,window_size,tempfname,f2d,extension="txt"):
    # Recursively find all *.txt files in **/usr/bin**.
    # f2d indicates how many files per dictionary (to process large collections)
    found_files = [f for f in locate("*"+extension,folder)]
    total_counter = process_file(found_files[0],window_size)
    tot_files = len(found_files)
    print "Found",tot_files,"Files"
    for i,f in enumerate(found_files[1:]):
        total_counter.update(process_file(f,window_size))
        if i%100 == 0:
            pprint(str(datetime.datetime.now())+":"+str(i)+"/"+str(tot_files)+" Files")
        if i%f2d==0 and i>0:
            pprint(str(datetime.datetime.now())+": Writing files "+str(i-f2d)+" to "+str(i))
            write_counter_b(tempfname+"_"+str(i)+".dat",total_counter)
            del total_counter
            total_counter = Counter()
    print "Done",tot_files,"Files",total_counter["@#total#@"],"Words",len(total_counter.keys())-total_counter["@#total#@"]-1,"pairs"
    return total_counter


def write_counter(outfilename,counter):
    testFile = open(outfilename, "w")
    #testFile.write(printHeader())
    wordListPrinter(counter, testFile)

def write_counter_b(outfilename,counter):
    of = open(outfilename,"w")
    cPickle.dump(counter,of,cPickle.HIGHEST_PROTOCOL)
    of.close()

if __name__=='__main__':
    script, folder, outfilename = argv
    counts = process_folder(folder,5,outfilename,1500,"")
    write_counter_b(outfilename,counts)


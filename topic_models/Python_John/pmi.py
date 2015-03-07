# -*- coding: utf-8 -*-
"""
John Hewitt
2/15/15
Writing a PMI to pass through text files
    -open file --done
    -need to get w1, w2 --done
    -import stopwords filter. remove all occurences of words that are in this set before we work more intensively with the calculations
    -find 
        --gram[] ; list of sample words, by window n -done
        --tot ; all words in sample space --word count, done
    -look for index of words and count occurences (Collection.counter(set)) -done
    -apply pmi -done
        --rinse, repeat pmi for all sets of words in text
    -print results
    -find a good threshold to return meaningful word pairs
    -apply threshold to filter out poor results
    -always close resources
    """

import math
from collections import Counter


#functions used by PMI, John Hewitt
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
   return open(filename).read().split(" ")
   
def wordCounter(l_words):
   return Counter(l_words)
   
#nested for loop goes through a string to retrieve all possible word pair combinations
def bigramCombination(listString):
    newList = []
    
    for e1 in listString[:-1]:
        for e2 in listString:
            newItem = [e1, e2]
            newList.append(newItem)
            
    return newList
    
#window shifter, gets first window, moves position by one, appends all combinations to the last element
#unfinished
def windowShift(listString, initialN):
   newList = []
   
   #first window
   for e1 in listString[:initialN - 1]:
      for e2 in listString[:initialN]:
         if(e1 != e2): 
            newItem = [e1, e2]
            newList.append(newItem)
         
   for e1 in listString[initialN:]:
      for e2 in listString:
         if(e1 != e2):
            newItem = [e1, e2]
            newList.append(newItem)      
   return newList


#open test file, and split it into words
fileName = "shiloh.txt"
fileFolder = [] #will implement later
wordList1 = file2list(fileName)
listString = "The battle of shiloh took place during the civil war" 
listString = listString.split(" ")
wordWindows = windowShift(wordList1, 4)
listWindow = windowShift(listString, 4)
#print wordWindows
print listWindow


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
#print wordListAndGrams """





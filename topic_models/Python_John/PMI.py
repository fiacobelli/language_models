# -*- coding: utf-8 -*-
"""
John Hewitt
#2/15/15
#Writing a PMI to pass through text files
    -open file
    -need to get w1, w2
    -find 
        --gram[] ; list of sample words, and the occurence of pairs
        --tot ; all words in sample space
    -look for index of words and count occurences
    -apply pmi
        --rinse, repeat pmi for all sets of words in text
    -print results
    -find a good threshold to return meaningful word pairs
    -apply threshold to filter out poor results
    -always close resources
    """
import math
import os


#Dr Francisco Iacobelli provided the PMI and N-grams functions
def pmi(w1, w2, grams, tot):
    return math.log(grams[w1 + " " + w2] * 1.0 / (grams[w1] * grams[w2]) * tot)
    
def ngrams (input , n):
    input = input.split('\u23B5')#can't seem to find the bottom square bracket working 
    output = []
    for i in range (len(input), n-1):
        output.append('\u23B5'.join(input [i:i+n]))
    return output


test_file = open('C:\\Users\\jhewi_000\\Documents\\GitHub\\language_models\\topic_models\\Python_John\\shiloh.txt')

f = test_file.read()

print f

word1_count = 0
word2_count = 0

#for each line in text
for line in f:
    #get word 1 and word 2 : ngrams, 
    #MAKE SURE EACH LINE FOR NGRAM IS A SENTENCE
    #may need to use a token for stopping the input, such as  . ! ? :, no numbers
    #search for w1, w2 in text
    #increment word1 and word2 counts, also w1 + " " + w2 counts
    #comparison, count w1 and w2 frequency
    #count all words
    #apply pmi
    #reset counters
    print ngrams(line, 4)
    
test_file.close()

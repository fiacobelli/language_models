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
import build_model as bm
import numpy

punct = re.compile(r'\W')
#functions used by PMI application from line 24 - 64
#Dr Francisco Iacobelli provided the PMI and N-grams functions
def pmi(w1, w2, grams, tot):
    key = w1 + " " + w2
    if key in grams:
        return math.log((grams[w1 + " " + w2] * 1.0) / (grams[w1] * grams[w2]) * tot)
    return 0


def ngrams(input, n):
    input = input.split(" ")
    output = []
    for i in range(len(input)- n + 1):
        output.append(" ".join(input [i:i+n]))
    return output

def read_model(filename):
    '''
        read the filename model and return a dictionary
    '''
    f = open(filename)
    counts = {}
    for line in f:
        key,val = line.split("\t")
        counts[key]=int(val)
    return counts

# According to Newman et al., PMI-score(sentence)=median{PMI(w_i,w_j), i,j in {1..window size}
def sentence_pmi(sentence,counts):
        tot = counts["@#total#@"]
        words = bm.normalize_words(sentence.split(" "))
        tot_pmi = []
        combos = bm.bigramCombination(words)
        for b in combos:
            w1,w2=b.split()
            tot_pmi.append(pmi(w1,w2,counts,tot))
        print tot_pmi
        return numpy.median(numpy.array(tot_pmi))


if __name__=='__main__':
    script, filename, sentence = argv
    m = read_model(filename)
    print(sentence_pmi(sentence,m))


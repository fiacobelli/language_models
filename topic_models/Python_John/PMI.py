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
import sys
import re
import build_model as bm
import numpy
import cPickle, datetime
import pprint

punct = re.compile(r'\W')
#functions used by PMI application from line 24 - 64
#Dr Francisco Iacobelli provided the PMI and N-grams functions
def pmi(w1, w2, grams, tot):
    key = w1 + " " + w2
    if key in grams:
        return math.log(float(grams[w1 + " " + w2])) / float(grams[w1] * grams[w2]) * tot)
    return 0.5/tot


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
    counts={}
    with open(filename) as f:
        i=0
        for line in f:
            key,val = line.split("\t")
            counts[key]=int(val)
            if i%10000==0:
                sys.stdout.write('[%s] %s ...%s\r' % (str(datetime.datetime.now()),"Pairs Read:",str(i)))
            i+=1
    return counts

def read_model_p(fname):
    f = open(fname,"rb")
    c = cPickle.load(f)
    f.close()
    return c

# According to Newman et al., PMI-score(sentence)=median{PMI(w_i,w_j), i,j in {1..window size}
def sentence_pmi(sentence,counts):
        tot = counts["@#total#@"]
        words = bm.normalize_words(sentence.strip().split(" "))
        tot_pmi = []
        combos = bm.bigramCombination(words)
        for b in combos:
            w1,w2=b.split()
            tot_pmi.append(pmi(w1,w2,counts,tot))
        tpmi= numpy.median(numpy.array(tot_pmi))
        #print "PMI for topic:",tpmi
        return tpmi


def topic_key_pmi(fname,counts):
    with open(fname) as f:
        tot_pmi=0.0
        num_t=1
        try:
            for topic in f:
                if len(topic)>10:
                    tot_pmi += sentence_pmi(topic2sentence(topic),counts)
                    num_t+=1
        except:
            print "File",fname,"Failed on topic",num_t
    return tot_pmi/num_t


def topic2sentence(topic):
    #print topic
    tn,prob,words = topic.split("\t")
    return words

def pmi_many_files(modelfile, filelist):
    print datetime.datetime.now(),"Reading model file"
    m = read_model(model)
    print datetime.datetime.now(), "Evaluating Topics"
    tfl=[(f,topic_key_pmi(f,m)) for f in filelist]
    pprint.pprint(tfl) 

if __name__=='__main__':
    model = sys.argv[1] #pass the model file
    files = sys.argv[2:] #then a bunch of files.
    print "Files",files
    pmi_many_files(model,files)


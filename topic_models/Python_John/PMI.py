# -*- coding: utf-8 -*-
"""
John Hewitt
#2/15/15
#Writing a PMI to pass through text files
    -open file --done
    -need to get w1, w2 --done
    -import stopwords filter. remove all occurences of words that are in this set before we work more intensively with the calculations
    -find 
        --gram[] ; list of sample words, by window n
        --tot ; all words in sample space --word count, done
    -look for index of words and count occurences (Collection.counter(set))
    -apply pmi
        --rinse, repeat pmi for all sets of words in text
    -print results
    -find a good threshold to return meaningful word pairs
    -apply threshold to filter out poor results
    -always close resources
    """
import math
import collections

#open test file
test_file = open('C:\\Users\\jhewi_000\\Documents\\GitHub\\language_models\\topic_models\\Python_John\\shiloh.txt')
total_words = wordCount(test_file)

#break file into words
f = test_file.read().split("\n")
frequencies_of_single_words = collections.counter(f)

#for each line in text
for line in f:
    #get word 1 and word 2 : ngrams, 
    #MAKE SURE EACH LINE FOR NGRAM IS A SENTENCE ... split(". ")
    #may need to use a token for stopping the input, such as  . ! ? :, no numbers
    #search for w1, w2 in text .. done
    #increment w1 + " " + w2 counts
    #comparison, count w1 and w2 frequency
    #count all words .. done
    #apply pmi
    gram = ngrams(line, 2)

    
test_file.close()

#functions used by PMI, John Hewitt
#Dr Francisco Iacobelli provided the PMI and N-grams functions
def pmi(w1, w2, grams, tot):
    #i believe this is unfinished since gram[w1 + w2] is a count of the pair of strings, whereas gram[w1], gram[w2] are counts of individual words
    # to find the count of n-grams of words we much first find the count of w1 ... wN pairs, which is more involved than single word counts and may benefit from a different collection / list
    #see nPairFrequencySearch
    return math.log((grams[w1 + " " + w2] * 1.0 / (grams[w1] * grams[w2])) * tot))

def nPairFrequencySearch(w1, w2, pair):
    """find occurences of ngram pairs
        build a set of pairs from w1, w2. call ngram for pair production
        return count of pairs of words for PMI function
        we have to organize a new collection that contains key/value pairs to use in PMI
        """


def ngrams(input, n):
    input = input.split(" ")
    output = []
    for i in range(len(input) - n+1):
        output.append(" ".join(input [i:i+n]))
    return output

#get total words, should be refined to include actual sentences
def wordCount(file):
    word_count = 0
    for sentence in file:
        words = sentence.split(" ")
        word_count += len(words) + 1 #account for zero index
    return word_count - 1

def remove_stopwords(file, stoplist):
    for word in file:
#remove stopwords that match the list of stopwords for each stopword

"""word_count = 0
    for word in f:
    word = word.split(" ")
    word_count += len(word) + 1
    #print f
    print word_count - 1 """
"""for word in gram:
    wordpair = word.split(" ")
    word1 = wordpair[0]
    word2 = wordpair[1] """
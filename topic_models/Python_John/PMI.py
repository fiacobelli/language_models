"""John Hewitt
#2/15/15
#Writing a PMI to pass through text files
    open file does not work, fix open file
    need to get w1, w2
    find 
        gram[] ; list of sample words, and the occurence of pairs
        tot ; all words in sample space
    look for index of words and count occurences
    apply pmi
    rinse, repeat pmi for all sets of words in text
    print results,
    find a good threshold to return meaningful word pairs
    apply threshold to filter out poor results
    always close resources
    """
import math

test_file = open('C:\Users\jhewi_000\Documents\GitHub\language_models\topic_models\Python_John\shiloh.txt', 'r')

word1 = test_file.read()
print word1

word1_count = 0
word2_count = 0
#for each line in text
    #get word 1 and word 2
    #search for w1, w2 in text
    #increment word1 and word2 counts, also w1 + " " + w2 counts
    #comparison, count w1 and w2 frequency
    #count all words
    #apply pmi
    #reset counters
test_file.close()

def pmi(w1, w2, grams, tot):
    return math.log(grams[w1 + " " + w2] * 1.0 / (grams[w1] *grams[w2]) * tot)
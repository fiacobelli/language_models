import os
import math
import numpy

def __calculate_average_pmi__(dir_file, ngrams):
    average_pmi = {}
    num_file = {}
    files_in_dir = os.listdir(dir_file)
    for f in files_in_dir:
        if f.endswith('.txt'):
            print f
            file_pmi = []
            num_topics = f.split('_')[2]
            indiv_file_pmi = f.split('_')[2] + "_" + f.split('_')[3]
            corpora_type = f.split('_')[0]
            lines = 0
            with open (dir_file + f) as file:
                for l in file:
                    words = [w.rstrip(',') for w in l.strip('\n').split(' ')[1:]]
                    file_pmi.append(calculate_topic_pmi(words, ngrams))
                    lines += 1
                if corpora_type in average_pmi:
                    if num_topics in average_pmi[corpora_type]:
                        average_pmi[corpora_type][num_topics] += sum(file_pmi)/lines
                        num_file[corpora_type][num_topics] += 1.0
                    else:
                        average_pmi[corpora_type][num_topics] = sum(file_pmi)/lines
                        num_file[corpora_type][num_topics] = 1.0
                else:
                    average_pmi[corpora_type] = {num_topics: sum(file_pmi)/lines}
                    num_file[corpora_type] = {num_topics: 1.0}

                average_pmi[corpora_type][indiv_file_pmi] = sum(file_pmi)/lines
                num_file[corpora_type][indiv_file_pmi] = 1

    for corp in average_pmi:
        for key in average_pmi[corp]:
            average_pmi[corp][key] = average_pmi[corp][key]/num_file[corp][key]
    return average_pmi


def calculate_topic_pmi(words, ngrams):
    pmi_topic = []
    for i, w1 in enumerate(words):
        for j, w2 in enumerate(words[i+1:]):
            if w1 in ngrams and w2 in ngrams and w1 + ' ' + w2 in ngrams:
                pmi_topic.append(math.log((ngrams[w1 + ' ' + w2] * ngrams["@#total#@"])/float(ngrams[w1] * ngrams[w2])))
            else:
                pmi_topic.append(0)
    return numpy.median(pmi_topic)



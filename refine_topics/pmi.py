import os


def __calculate_average_pmi__(dir_file, ngrams):
    average_pmi = {}
    num_file = {}
    files_in_dir = os.listdir(dir_file)
    for f in files_in_dir:
        if f.endswith('.txt'):
            file_pmi = []
            num_topics = int(f.split('_')[2])
            with open (dir_file + f) as file:
                for l in file:
                    words = [w.rstrip(',') for w in l.strip('\n').split(' ')[1:]]
                    file_pmi.append(calculate_topic_pmi(words, ngrams))
                if num_topics in average_pmi:
                    average_pmi[num_topics] += sum(file_pmi)/int(num_topics)
                    num_file[num_topics] += 1.0
                else:
                    average_pmi[num_topics] = sum(file_pmi)/int(num_topics)
                    num_file[num_topics] = 2.0
    for key in average_pmi:
        average_pmi[key] = average_pmi[key]/num_file[key]
    return average_pmi


def calculate_topic_pmi(words, ngrams):
    pmi_topic = []
    for i, w1 in enumerate(words):
        for j, w2 in enumerate(words[i+1:]):
            if w1 in ngrams and w2 in ngrams and w1 + ' ' + w2 in ngrams:
                pmi_topic.append(ngrams[w1 + ' ' + w2]/float(ngrams[w1] * ngrams[w2]))
                print w1 + ' ' + w2
            else:
                pmi_topic.append(0)
    print words
    print sum(pmi_topic)/sum([i for i in range(len(words))])
    return sum(pmi_topic)/sum([i for i in range(len(words))])



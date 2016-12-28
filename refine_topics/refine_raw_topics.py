import math
import numpy as np
#import matplotlib.pyplot as plt


def __save_topic__(dir_name, topics_prob_matrix, perc):
    f = open(dir_name, 'w')
    topics_prob_matrix = zip(*topics_prob_matrix)
    garbage_topics = find_garbage_topics(topics_prob_matrix, perc)
    topics_prob_matrix = remove_garbage_topics(topics_prob_matrix, garbage_topics)
    for i, topic_row in enumerate(topics_prob_matrix[1:]):
        words = [x for (y, x) in sorted(zip(topic_row, topics_prob_matrix[0]), reverse=True)]
        word_prob = sorted(topic_row, reverse=True)
        stop_index = word_prob.index(0)
        f.write(str(i) + ' ' + (', '.join(words[:10]))+'\n')
    f.close()

'''
each topic is made up of words and words each topic word cell has a probability associated to it
topic# word1 word2 word3
This function will decide whether the topic should be trashed or not
'''
def find_garbage_topics(topics_prob_matrix, perc):
    kb_divergence = []
    for topics_row in topics_prob_matrix[1:]:
        #each topic has a uniform probability which is the 1/sum of the probabilities making up x percentage of the topic
        uniform_prob = find_uniform_prob(topics_row, perc)
        #find how muchthe original probabilities of the words in the topics diverge from its uniform divergence.
        kb_divergence.append(find_topic_kb_divergence(topics_row, uniform_prob))
    std = np.std(kb_divergence)
    mean = np.mean(kb_divergence)
    min_norm = mean - std
    max_norm = mean + std
    garbage_topics =[]
    for i, d in enumerate(kb_divergence):
        if min_norm <= d <= max_norm:
            garbage_topics.append(i)
    return garbage_topics


def find_uniform_prob(topic_row, prob_perc):
    topic_row = sorted(topic_row, reverse=True)
    for i, p in enumerate(topic_row):
        if prob_perc <= 0:
            return 1.0/i
        prob_perc -= p
    return 1.0/len(topic_row)


def find_topic_kb_divergence(topic_row, uniform_prob):
    divergence = 0
    for p in topic_row:
        if p > 0:
            divergence += p * math.log(p/uniform_prob)
    return divergence


def remove_garbage_topics(topics_prob, garbage_topics):
    garbage_topics = sorted(garbage_topics, reverse=True)
    for g in garbage_topics:
        topics_prob.pop(g + 1)
    return topics_prob


'''def __graph_topic_against_uniform_prob__(topics_prob_matrix, topic_index):
    topics_prob_matrix = zip(*topics_prob_matrix)
    for i, topic_row in enumerate(topics_prob_matrix[1:]):
        if i == topic_index:
            word_count = len(topic_row)
            uniform_prob = find_uniform_prob(topic_row)
            uniform_prob = word_count * [uniform_prob]
            plt.plot(range(word_count), topic_row)
            plt.plot(range(word_count), uniform_prob)
            plt.show()
            break

'''
def load_prob_matrix(dir_name):
    topics_prob_matrix = []
    with open(dir_name) as f:
        for l in f:
            topics_prob_matrix.append([l.strip().split(',')[0]] + [float(p) for p in l.strip().split(',')[1:]])
    return topics_prob_matrix


if __name__ == '__main__':

    import argparse

    args = argparse.ArgumentParser('Removes garbage topics and saves them.')
    args.add_argument('input', help='The location of the csv file containing topics word probability matrix.')
    args.add_argument('output', help='The location for saving the refined topics text file.')
    args.add_argument('perc', help='Total probability of words to be considered in finding the uniform topic.')

    values = args.parse_args()
    topics_prob_matrix = load_prob_matrix(values.input)
    __save_topic__(values.output, topics_prob_matrix, float(values.perc)/100)



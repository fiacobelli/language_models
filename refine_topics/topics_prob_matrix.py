import csv


def __create_topic_matrix__(file_dir, distribution_type, num_topics):
    count_topics = []
    word_count = 0
    with open(file_dir) as f:
        for l in f:
            word_count += 1
            l_parts = l.split()
            parts_length = len(l_parts)
            if parts_length > 2:
                count_topics.append(create_word_count_row(l_parts[1:], num_topics))
        if distribution_type == 1:
            return find_prob_topic_wise(count_topics)
        elif distribution_type == 2:
            return find_prob_word_wise(count_topics)
        else:
            return find_prob_document_wise(count_topics, word_count)
        f.close()


def create_word_count_row(l_parts, num_topics):
    word_row = [0] * (num_topics + 1)
    word_row[0] = l_parts[0]
    for p in l_parts[1:]:
        topic_index = int(p.split(':')[0])
        word_count = float(p.split(':')[1])
        word_row[topic_index + 1] = word_count
    return word_row


def find_prob_topic_wise(count_topics):
    prob_topics = []
    for word_row in count_topics:
        total_count = sum(word_row[1:])
        prob_topics.append([word_row[0]] + [float(c)/total_count for c in word_row[1:]])
    return prob_topics


def find_prob_word_wise(count_topics):
    count_topics = zip(*count_topics)
    prob_topics = []
    for topic_row in count_topics[1:]:
        total_count = sum(topic_row)
        prob_topics.append([float(c)/total_count for c in topic_row])
    prob_topics.insert(0, count_topics[0])
    return zip(*prob_topics)


def find_prob_document_wise(count_topics, total_words):
    prob_topics = []
    for word_row in count_topics:
        prob_topics.append([word_row[0]] + [float(c)/total_words for c in word_row[1:]])
    return prob_topics


def __save_prob_matrix__(file_dir, prob_matrix):
    with open(file_dir, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(prob_matrix)
        f.close()


if __name__ == '__main__':

    import argparse

    args = argparse.ArgumentParser('Creates a csv file containing topics, words adn their probabilities.')
    args.add_argument('input', help='Location of the file with words and their occurrences in topics.')
    args.add_argument('output', help='The location for saving the probability matrix file of the topics')
    args.add_argument('num', help='Number of topics in file.')
    args.add_argument('distribution', help='1. Calculate probabilities topic-wise where the total probability of a word'
                                           'in all topics together will be equal to 1. It is the probability of a word '
                                           'being in a topic compared to all other topics.'
                                           '2. Calculate probabilities word-wise where the total probability of all '
                                           'words in a single topics together will be equal to 1. It is the '
                                           'probability of a word being in a topic compared to all other words in '
                                           'that topic.'
                                           '3. Calculate probability document-wise where the total probability of '
                                           'all the words in the document will together equal to 1. It is the '
                                           'probability of the word being in the document compared to all the words.'
                                           'in the document')
    values = args.parse_args()
    topic_prob_matrix = __create_topic_matrix__(values.input, int(values.distribution), int(values.num))
    __save_prob_matrix__(values.output, topic_prob_matrix)




def __save_topic__(dir_name, topics_prob_matrix):
    f = open(dir_name, 'w')
    topics_prob_matrix = zip(*topics_prob_matrix)
    for i, topic_row in enumerate(topics_prob_matrix[1:]):
        words = [x for (y, x) in sorted(zip(topic_row, topics_prob_matrix[0]), reverse=True)]
        word_prob = sorted(topic_row, reverse=True)
        stop_index = word_prob.index(0)
        f.write(str(i) + ' ' + (', '.join(words[:10]))+'\n')
    f.close()


def load_prob_matrix(dir_name):
    topics_prob_matrix = []
    with open(dir_name) as f:
        for l in f:
            topics_prob_matrix.append([l.strip().split(',')[0]] + [float(p) for p in l.strip().split(',')[1:]])
    return topics_prob_matrix


if __name__ == '__main__':

    import argparse

    args = argparse.ArgumentParser('Creates topics.')
    args.add_argument('input', help='The location of the csv file containing topics word probability matrix.')
    args.add_argument('output', help='The location for saving the topics text file.')

    values = args.parse_args()
    topics_prob_matrix = load_prob_matrix(values.input)
    __save_topic__(values.output, topics_prob_matrix)





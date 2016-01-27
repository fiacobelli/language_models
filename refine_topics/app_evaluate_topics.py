import topics_prob_matrix as tpm
import extract_raw_topics as ert
import refine_raw_topics as rrt


if __name__ == '__main__':

    import argparse

    args = argparse.ArgumentParser('Generates topics, refined topics and finds pmi for each refined topic.')
    args.add_argument('input_raw', help='Location of the file with words and their occurrences in topics.')
    args.add_argument('output_topics', help='The location for saving the topics text file.')
    args.add_argument('output_refined', help='The location for saving the refined topics text file.')
    args.add_argument('num', help='Number of topics in file.')
    args.add_argument('perc', help='Total probability of words to be considered in finding the uniform topic.')

    values = args.parse_args()
    topic_prob_matrix = tpm.__create_topic_matrix__(values.input_raw, 2, int(values.num))
    ert.__save_topic__(values.output_topics, topic_prob_matrix)
    rrt.__save_topic__(values.output_refined, topic_prob_matrix, 100)

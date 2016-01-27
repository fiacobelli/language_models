import topics_prob_matrix as tpm
import extract_raw_topics as ert
import refine_raw_topics as rrt
import ngrams as ng
import pmi
import os
import json


if __name__ == '__main__':

    import argparse

    args = argparse.ArgumentParser('Generates topics, refined topics and finds pmi for each refined topic.')
    args.add_argument('input_wiki', help='File containing unigrams and bigrams to train pmi.')
    args.add_argument('input_raw', help='Folder that contains the files of words and their occurrences in topics (raw topics.')
    args.add_argument('output_topics', help='Folder where topics text files will be saved.')
    args.add_argument('output_refined', help='Folder where refined topics text files will be saved.')
    args.add_argument('output_pmi', help='File to save average pmi of files with different number of topics.')
    args.add_argument('perc', help='Total probability of words to be considered in finding the uniform topic.')

    values = args.parse_args()

    files_in_dir = os.listdir(values.input_raw)
    for f in files_in_dir:
        if f.endswith('.txt'):
            f_parts = f.split('_')
            num_topics = int(f_parts[2])
            topic_prob_matrix = tpm.__create_topic_matrix__(values.input_raw + f, 2, num_topics)
            ert.__save_topic__(values.output_topics + f, topic_prob_matrix)
            rrt.__save_topic__(values.output_refined + f, topic_prob_matrix, float(values.perc)/100)
            ngrams = ng.__read_ngrams__(values.input_wiki)
            pmi_dict = pmi.__calculate_average_pmi__(values.output_refined, ngrams)
            json.dump(pmi_dict, open(values.output_pmi, 'w'))





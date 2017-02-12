import topics_prob_matrix as tpm
import extract_raw_topics as ert
import refine_raw_topics as rrt
import deletedtopics as dt
import ngrams as ng
import pmi
import os
import json


if __name__ == '__main__':

    import argparse

    args = argparse.ArgumentParser('Generates topics, refined topics and finds pmi for each refined topic.')
    args.add_argument('training_wiki_file', help='File containing unigrams and bigrams to train pmi.')
    args.add_argument('mallet_topics_dir', help='Folder that contains the files of words and their occurrences in topics (raw topics.')
    args.add_argument('raw_topics_dir', help='Folder where topics text files will be saved.')
    args.add_argument('refined_topics_dir', help='Folder where refined topics text files will be saved.')
    args.add_argument('del_topics_dir', help='File to save average pmi of files refined with different number of topics.')
    args.add_argument('raw_pmi_file', help='File to save average pmi of files with raw topics and different number of topics.')
    args.add_argument('refined_pmi_file', help='File to save average pmi of files refined with different number of topics.')
    args.add_argument('perc', help='Total probability of words to be considered in finding the uniform topic.')


    values = args.parse_args()

    files_in_dir = os.listdir(values.mallet_topics_dir)
    ngrams = ng.__read_ngrams__(values.training_wiki_file)
    print ("Finished reading ngrams..")
    for f in files_in_dir:
        if f.endswith('.txt'):
            f_parts = f.split('_')
            num_topics = int(f_parts[2])
            topic_prob_matrix = tpm.__create_topic_matrix__(values.mallet_topics_dir + f, 2, num_topics)
            ert.__save_topic__(values.raw_topics_dir + f, topic_prob_matrix)
            rrt.__save_topic__(values.refined_topics_dir + f, topic_prob_matrix, float(values.perc)/100)
    print ("Finished extracting and saving raw and refined topics..")
    pmi_dict = pmi.__calculate_average_pmi__(values.refined_topics_dir, ngrams)
    json.dump(pmi_dict, open(values.refined_pmi_file, 'w'))
    print ("Finished calculating pmi for refined topics..")
    pmi_dict = pmi.__calculate_average_pmi__(values.raw_topics_dir, ngrams)
    json.dump(pmi_dict, open(values.raw_pmi_file, 'w'))
    print ("Finished calculating pmi for raw topics..")
    dt.getDiff(values.raw_topics_dir, values.refined_topics_dir, values.del_topics_dir)




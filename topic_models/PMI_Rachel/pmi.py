import os
import glob
import argparse
import datetime
import logging
from datetime import datetime as dt
from text_parser import TextParser
from corpora import Corpora
from corpora_matrix import CorporaMatrix
from pmi_calculator import PmiCalculator

logging.basicConfig(filename='pmi-script.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)

def main(args):
  start = dt.now()
  choose_action(args)
  stop = dt.now()
  logging.info('Time Elapsed:%s'%str(datetime.timedelta(seconds = (stop - start).total_seconds())))

def choose_action(args):
  if args.action is 'c': create_word_dictionary_and_matrix(args)
  if args.action is 'r': calculate_topic_pmis(args)

def create_word_dictionary_and_matrix(args):
  parser = TextParser(args.remove_stopwords)
  corpora = Corpora()
  matrix = CorporaMatrix(args.s)
  logging.info("Reading files...")
  file_num = 1
  for infile in glob.iglob(os.path.join(args.input_path, '*.txt')):
    logging.debug("Reading file number %d. So far: words:%d, pairs:%d", file_num,len(corpora.word_dict.keys()),len(matrix.word_matrix.keys()))
    open_and_read_file(infile, parser, corpora, matrix)
    file_num += 1

  logging.info("Serializing corpora dictionary with %d words"%len(corpora.word_dict.keys()))
  corpora.serialize_dict(args.output_path)
  logging.info("Serializing corpora matrix with %d pairs"%len(matrix.word_matrix.keys()))
  matrix.serialize_matrix(args.output_path)

def open_and_read_file(infile, parser, corpora, matrix):
  with open(infile, 'r') as open_file:
    f = open_file.read().split("\n")
    for line in f:
      text = parser.parse_line(line)
      corpora.create_dictionary(text)
      matrix.count_coocurrences(corpora.word_dict, text)

def calculate_topic_pmis(args):
  word_dict = Corpora().deserialize_dict(args.word_dict)
  word_matrix = CorporaMatrix().deserialize_matrix(args.word_matrix)
  logging.info('Calculating PMIs...')
  PmiCalculator(word_dict, word_matrix, args.topic_words.split(' '), args.output_path).calculate_pmis()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description = 'Open a directory for reading a corpora matrix or creating a corpora matrix.')
  parser.add_argument('action', choices = ['c', 'r'], help = 'Creating a matrix: c, Reading a matrix: r')
  parser.add_argument('--input_path', help = 'The directory where the file corpora are located')
  parser.add_argument('--output_path', default = '', help = 'The output directory for the output files')
  parser.add_argument('--remove_stopwords', default = 'y', choices = ['y', 'n'], help = 'Determines whether or not to remove stop words from the corpora')
  parser.add_argument('--word_dict', help = 'The complete path for the word dictionary file, required when using the r option')
  parser.add_argument('--word_matrix', help = 'The complete path for the word matrix file, required when using the r option')
  parser.add_argument('--topic_words', help = 'A string of the topic words that should be enclosed in double quotes and separated by spaces, required when using the r option')
  parser.add_argument('--s', default = 1, help = 'The number of words by which the text window slides in order to create the frequency matrix')
  args = parser.parse_args()
  main(args)

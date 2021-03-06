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
import sqlite3

logging.basicConfig(filename='pmi-script.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)

# This program is a subset of the main pmi.py. It is geared to corpora where each line is a set of words and the last item is the 
# frequency of the ngram.
def main(args):
  start = dt.now()
  choose_action(args)
  stop = dt.now()
  logging.info('Time Elapsed:%s'%str(datetime.timedelta(seconds = (stop - start).total_seconds())))

def choose_action(args):
  #if args.action is 'c': create_word_dictionary_and_matrix(args)
  if args.action is 'r': calculate_topic_pmis(args)

def create_word_dictionary_and_matrix(args):
  parser = TextParser(args.remove_stopwords)
  corpora = Corpora()
  matrix = CorporaMatrix(args.s)
  conn = sqlite3.connect(args.word_matrix+'5gms_db.db')
  c = conn.cursor()
#  c.execute('''DROP TABLE IF EXISTS five_grams''')
#  c.execute('''CREATE TABLE five_grams (id1 INT,id2 INT, id3 INT, id4 INT, id5 INT, freq INT)''');
  
  logging.info("Reading word Dictionary")
  word_dict = Corpora().deserialize_dict(args.word_dict) #assumes word_dict to be in output path.
  logging.info("Reading files...")
  file_num = 1
  for infile in glob.iglob(os.path.join(args.input_path, '*.txt')):
    logging.debug("Reading file number %d. So far: words:%d, ngrams:%d", file_num,len(word_dict.keys()),len(matrix.fast_matrix))
    open_and_read_file(infile, parser, word_dict, matrix,c)
    conn.commit()
    file_num += 1
  conn.close()

  logging.info("Serializing corpora dictionary with %d words"%len(corpora.word_dict.keys()))
  corpora.serialize_dict(args.output_path)
  logging.info("Serializing corpora matrix with %d pairs"%len(matrix.word_matrix.keys()))
  matrix.serialize_matrix(args.output_path)

def open_and_read_file(infile, parser, word_dict, matrix,c):
  inserts = []
  add_val = inserts.append
#  word_dict = corpora.word_dict
  with open(infile, 'r') as open_file:
    for line in open_file:
      text = parser.parse_line(line)
      # last item in text is a frequency
      # create_d(text[:-1])
      if (len(text)==6 and text[-1].isdigit()):
        tmp = [word_dict[w][1] for w in text[:-1]]
        tmp.append(text[-1])
        add_val(tuple(tmp))
#        matrix.add_key_count_fast(corpora.word_dict, text[:-1],int(text[-1]))
    c.executemany("INSERT INTO five_grams VALUES(?,?,?,?,?,?)",inserts)

def calculate_topic_pmis(args):
  conn = sqlite3.connect('/Users/fdiacobe/research/topicModelEval/data/5gms_db.db')
  c = conn.cursor()
  word_dict = Corpora().deserialize_dict(args.word_dict)
  #word_matrix = CorporaMatrix().deserialize_matrix(args.word_matrix)
  logging.info('Calculating PMIs...')
  pmis = PmiCalculator(word_dict, c, args.topic_words.split(' '), args.output_path).calculate_pmis_db()
  print pmis


#def create_db():
#    conn = sqlite3.connect('5gms_db_idx.db')
#    c = conn.cursor()
#    c.execute('''DROP TABLE IF EXISTS five_grams''')
#    c.execute('''CREATE TABLE five_grams (id1 INT,id2 INT, id3 INT, id4 INT, id5 INT, freq INT)''')
# indices                                                                                                                         
#    c.execute("CREATE INDEX id1_2 on five_grams (id1,id2)")
#    c.execute("CREATE INDEX id1_3 on five_grams (id1,id3)")
#    c.execute("CREATE INDEX id1_4 on five_grams (id1,id4)")
#    c.execute("CREATE INDEX id1_5 on five_grams (id1,id5)")
#    c.execute("CREATE INDEX id2_3 on five_grams (id2,id3)")
#    c.execute("CREATE INDEX id2_4 on five_grams (id2,id4)")
#    c.execute("CREATE INDEX id2_5 on five_grams (id2,id5)")
#    c.execute("CREATE INDEX id3_1 on five_grams (id3,id4)")
#    c.execute("CREATE INDEX id3_2 on five_grams (id3,id5)")
#    c.execute("CREATE INDEX id4_5 on five_grams (id4,id5)")
#    c.execute("PRAGMA synchronous=OFF")
#    c.execute("PRAGMA journal_mode=OFF")
#    c.execute("PRAGMA cache_size=4000")                                                                                                          
#    conn.commit()                                                                                                                                
#    conn.close()

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

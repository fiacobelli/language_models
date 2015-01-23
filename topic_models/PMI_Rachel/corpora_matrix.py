import pickle
import os
import itertools
import sqlite3

class CorporaMatrix:

  def __init__(self, slide_size):
    self.word_matrix = {}
    self.fast_matrix = []
    self.slide_size = slide_size

  def count_coocurrences(self, word_dict, text):
    if len(text)<5:
      word_pairs = itertools.combinations(text,2)
      self.iterate_through_word_pairs(word_pairs,word_dict)
    else:
      for index in xrange(0, len(text) - 4, self.slide_size):
        window = text[index:index + 5]
        word_pairs = itertools.combinations(window, 2)
        self.iterate_through_word_pairs(word_pairs, word_dict)

  def iterate_through_word_pairs(self, word_pairs, word_dict):
    for wordi, wordj in word_pairs:
      id_i = word_dict[wordi][1]
      id_j = word_dict[wordj][1]
      self.add_to_matrix(id_i, id_j)

  def add_to_matrix(self, id_i, id_j):
    if self.word_matrix.has_key((id_i, id_j)):
      self.word_matrix[(id_i, id_j)] += 1
    elif self.word_matrix.has_key((id_j, id_i)):
      self.word_matrix[(id_j, id_i)] += 1
    else:
      self.word_matrix[(id_i, id_j)] = 1

  def add_key_with_count(self, word_dict,text,freq):
    t = self.text_to_tuple(text,word_dict)
    if self.word_matrix.has_key(t):
      self.word_matrix[t]+=freq
    else:
      self.word_matrix[t]=freq

  def add_key_count_fast(self,word_dict,text,freq):
    self.fast_matrix.append([self.text_to_tuple(text,word_dict),freq])


  def add_counts_to_db(self,word_dict,text,freq):
    text.append(freq)
    t = self.text_to_tuple(text,word_dict)
    self.c.execute("INSERT INTO 5grams VALUES"+str(t))

  def text_to_tuple(self,text,word_dict):
    tmp = [word_dict[w][1] for w in text]
    return tuple(tmp)


  def serialize_matrix(self, output_path):
    pickle.dump(self.word_matrix, open(os.path.join(output_path, 'word_matrix.txt'), 'wb'))

  def serialize_fast_matrix(self,output_path):
    pickle.dump(self.fast_matrix,open(os.path.join(output_path, 'fast_word_matrix.txt'),'wb'))

  def deserialize_matrix(self, input_file):
    return pickle.load(open(os.path.abspath(input_file), 'rb'))

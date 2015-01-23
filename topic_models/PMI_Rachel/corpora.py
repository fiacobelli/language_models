import pickle
import os

class Corpora:

  def __init__(self):
    self.word_dict = {}
    self.count = 0

  def create_dictionary(self, text):
    for word in text:
      self.add_to_dict(word)

  def add_to_dict(self, word):
    if self.word_dict.has_key(word):
      self.word_dict[word][0] += 1
    else:
      self.word_dict[word] = [1, self.count]
      self.count += 1

  def serialize_dict(self, output_path):
    pickle.dump(self.word_dict, open(os.path.join(output_path, 'word_dict.txt'), 'wb'))

  def deserialize_dict(self, input_file):
    return pickle.load(open(os.path.abspath(input_file), 'rb'))

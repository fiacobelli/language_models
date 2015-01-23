import string
import re

class TextParser:

  def __init__(self, rm_stop_words):
    self.text = []
    if rm_stop_words is 'y': 
      self.stop_words = self.open_stop_file()
    else:
      self.stop_words = None

  def open_stop_file(self):
    stop_file = open('en.txt')
    stop_words =[line.rstrip() for line in open('en.txt')]
    return stop_words

  def parse_line(self, line):
    line_no_punc = line.translate(string.maketrans("",""), string.punctuation).lower()
    if self.stop_words:
      self.remove_stopwords(line_no_punc)
    else:
      self.text = line_no_punc.split()
    return self.text

  def remove_stopwords(self, line_no_punc):
    for word in line_no_punc.split():
      if word not in self.stop_words:
        self.text.append(word)

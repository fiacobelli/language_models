import itertools
from math import log
import os
import numpy

class PmiCalculator:

  def __init__(self, word_dict, crsr, topic_words, output_path):
    self.word_dict = word_dict
    self.crsr = crsr
    self.topic_words = topic_words
    self.all_pmis = []
    self.total_words = len(self.word_dict)
    self.output_path = os.path.abspath(output_path)
    self.selects = [["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id1=? and id2=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id1=? and id3=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id1=? and id4=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id1=? and id5=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id2=? and id1=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id2=? and id3=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id2=? and id4=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id2=? and id5=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id3=? and id1=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id3=? and id2=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id3=? and id4=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id3=? and id5=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id4=? and id1=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id4=? and id2=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id4=? and id3=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id4=? and id5=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id5=? and id1=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id5=? and id2=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id5=? and id3=?)"],
                    ["SELECT SUM(freq) as cofreq FROM five_grams WHERE (id5=? and id4=?)"],]

  def calculate_pmis_db(self):
    word_pairs = itertools.combinations(self.topic_words,2)
    pmis=[]
    for wordi, wordj in word_pairs:
      [freqi, freqj, cofreq] = self.find_freqs_in_db(wordi, wordj)
      pmis.append(self.calculate_pmi(freqi, freqj, cofreq))
    return pmis
      

  def write_pmis(self):
    output_file = self.open_and_write_header()
    self.find_freq_per_pair(itertools.combinations(self.topic_words, 2), output_file)
    self.write_last_line_and_close(output_file)

  def open_and_write_header(self):
    output_file = open(os.path.join(self.output_path, 'pmi_calcs.txt'), 'w')
    output_file.write('wordi \t wordj \t pmi \t freqi \t freqj \t cofreq \n')
    return output_file

  def find_freq_per_pair(self, word_pairs, output_file,ff):
    for wordi, wordj in word_pairs:
      [freqi, freqj, cofreq] = ff(wordi, wordj)
      pmi = self.calculate_pmi(freqi, freqj, cofreq)
      self.all_pmis.append(pmi)
      output_file.write(wordi + '\t' + wordj + '\t' + "{:.5f}".format(pmi) + '\t' + str(freqi) + '\t' + str(freqj) + '\t' + str(cofreq) + '\n')

  def find_freqs_in_db(self, wordi, wordj):
    w1 = self.word_dict[wordi][1]
    w2 = self.word_dict[wordj][1]
    cof = 0
    for selstr in self.selects:
        print selstr,wordi,w1,wordj,w2
        self.crsr.execute(selstr[0],(w1,w2))
        row = self.crsr.fetchone()
        cof += row[0] if row[0] is not None else 0
    return (self.word_dict[wordi][1],self.word_dict[wordj][1],cof)

  def find_freqs_in_dict(self, wordi, wordj):
    [freqi, id_i] = self.word_dict[wordi]
    [freqj, id_j] = self.word_dict[wordj]
    cofreq = self.find_cofreq(id_i, id_j)
    return [freqi, freqj, cofreq]

  def find_cofreq(self, id_i, id_j):
    if (id_i, id_j) in self.word_matrix:
      return self.word_matrix[(id_i, id_j)]
    elif (id_j, id_i) in self.word_matrix:
      return self.word_matrix[(id_j, id_i)]
    else:
      return 0

  def calculate_pmi(self, freqi, freqj, cofreq):
    if cofreq == 0: return 0
    return log(float(cofreq * self.total_words)/float(freqi * freqj))

  def write_last_line_and_close(self, output_file):
    output_file.write('\n\n')
    output_file.write('PMI median is: ' + "{:.5f}".format(numpy.median(self.all_pmis)))
    output_file.close()

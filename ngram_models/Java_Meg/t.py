#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

"""
This code implements a basic, Twitter-aware tokenizer.

A tokenizer is a function that splits a string of text into words. In
Python terms, we map string and unicode objects into lists of unicode
objects.

There is not a single right way to do tokenizing. The best method
depends on the application.  This tokenizer is designed to be flexible
and this easy to adapt to new domains and tasks.  The basic logic is
this:

1. The tuple regex_strings defines a list of regular expression
   strings.

2. The regex_strings strings are put, in order, into a compiled
   regular expression object called word_re.

3. The tokenization is done by word_re.findall(s), where s is the
   user-supplied string, inside the tokenize() method of the class
   Tokenizer.

4. When instantiating Tokenizer objects, there is a single option:
   preserve_case.  By default, it is set to True. If it is set to
   False, then the tokenizer will downcase everything except for
   emoticons.

The __main__ method illustrates by tokenizing a few examples.

I've also included a Tokenizer method tokenize_random_tweet(). If the
twitter library is installed (http://code.google.com/p/python-twitter/)
and Twitter is cooperating, then it should tokenize a random
English-language tweet.
"""

__authors__ = "Christopher Potts, Meg Ford"
__copyright__ = "Copyright 2011, Christopher Potts \n Copyright 2014 Meg Ford"
__credits__ = []
__license__ = "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License: http://creativecommons.org/licenses/by-nc-sa/3.0/"
__version__ = "1.0"
__maintainer__ = "Christopher Potts"
__email__ = "See the author's website"

######################################################################

import collections
from collections import defaultdict
import htmlentitydefs
import operator
import os
from os import listdir
from os.path import isfile, join
import re

######################################################################
# The following strings are components in the regular expression
# that is used for tokenizing. It's important that phone_number
# appears first in the final regex (since it can contain whitespace).
# It also could matter that tags comes after emoticons, due to the
# possibility of having text like
#
#     <:| and some text >:)
#
# Most imporatantly, the final element should always be last, since it
# does a last ditch whitespace-based tokenization of whatever is left.

# This particular element is used in a couple ways, so we define it
# with a name:
emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth    
      |
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""
username_string = r"""(?:@[\w_]+)"""
hashtag_string = r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
sentence_end =  r"""(?:[a-z]+[\.\?!]+[ ])""" 
url_string =  r"""(?:[htp]+[s]?[:/]+[a-z0-9]+[\w\d\.a-z/\?\=\&%\-]*)""" 
# The components of the tokenizer:
regex_strings = (
    # Phone numbers:
    r"""
    (?:
      (?:            # (international)
        \+?[01]
        [\-\s.]*
      )?            
      (?:            # (area code)
        [\(]?
        \d{3}
        [\-\s.\)]*
      )?    
      \d{3}          # exchange
      [\-\s.]*   
      \d{4}          # base
    )"""
    ,
    # Emoticons:
    emoticon_string
    ,    
    # HTML tags:
     r"""<[^>]+>"""
    ,
    # Twitter username:
    username_string
    ,
    # Twitter hashtags:
    hashtag_string
    ,
    # Last word in a sentence
    sentence_end
    ,
    #url
    url_string
    ,
    # Remaining word types:
    r"""
    (?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots. 
    #| 
    #(?:\S)                         # Everything else that isn't whitespace.
    """
    )

######################################################################
# This is the core tokenizing regex:
    
word_re = re.compile(r"""(%s)""" % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)

# The special strings gets their own regexes so that we can tag them as needed:
emoticon_re = re.compile(regex_strings[1], re.VERBOSE | re.I | re.UNICODE)
username_re = re.compile(regex_strings[3], re.VERBOSE | re.I | re.UNICODE)
hashtag_re = re.compile(regex_strings[4], re.VERBOSE | re.I | re.UNICODE)
sentence_end_re = re.compile(regex_strings[5], re.VERBOSE | re.I | re.UNICODE)
url_re = re.compile(regex_strings[6], re.VERBOSE | re.I | re.UNICODE)

# These are for regularizing HTML entities to Unicode:
html_entity_digit_re = re.compile(r"&#\d+;")
html_entity_alpha_re = re.compile(r"&\w+;")
amp = "&amp;"

######################################################################

class Tokenizer:
    def __init__(self, preserve_case=False):
        self.preserve_case = preserve_case

    def tokenize(self, s):
        """
        Argument: s -- any string or unicode object
        Value: a tokenize list of strings; conatenating this list returns the original string if preserve_case=False
        """        
        # Try to ensure unicode:
        try:
            s = unicode(s)
        except UnicodeDecodeError:
            s = str(s).encode('string_escape')
            s = unicode(s)
        # Fix HTML character entitites:
        s = self.__html2unicode(s)
        # Tokenize:
        words = word_re.findall(s)
        # Possible alter the case, but avoid changing emoticons like :D into :d:
        if not self.preserve_case:
          words = map(lambda x : self.replace_special(x), words)
        return words

    def tokenize_random_tweet(self):
        """
        If the twitter library is installed and a twitter connection
        can be established, then tokenize a random tweet.
        """
        try:
            import twitter
        except ImportError:
            print "Apologies. The random tweet functionality requires the Python twitter library: http://code.google.com/p/python-twitter/"
        from random import shuffle
        api = twitter.Api()
        tweets = api.GetPublicTimeline()
        if tweets:
            for tweet in tweets:
                if tweet.user.lang == 'en':            
                    return self.tokenize(tweet.text)
        else:
            raise Exception("Apologies. I couldn't get Twitter to give me a public English-language tweet. Perhaps try again")

    def __html2unicode(self, s):
        """
        Internal metod that seeks to replace all the HTML entities in
        s with their corresponding unicode characters.
        """
        # First the digits:
        ents = set(html_entity_digit_re.findall(s))
        if len(ents) > 0:
            for ent in ents:
                entnum = ent[2:-1]
                try:
                    entnum = int(entnum)
                    s = s.replace(ent, unichr(entnum))	
                except:
                    pass
        # Now the alpha versions:
        ents = set(html_entity_alpha_re.findall(s))
        ents = filter((lambda x : x != amp), ents)
        for ent in ents:
            entname = ent[1:-1]
            try:            
                s = s.replace(ent, unichr(htmlentitydefs.name2codepoint[entname]))
            except:
                pass                    
            s = s.replace(amp, " and ")
        return s
       
    def replace_special(self, word):
        if url_re.search(word):
            word = "url " #+ word
        elif emoticon_re.search(word):
            word = "emoticon " # +word (for testing)
        elif username_re.search(word):
            word = "username " #+ word
        elif hashtag_re.search(word):
            word = "hashtag " #+ word
        elif sentence_end_re.search(word):
            word = word
        return word.lower()

class NGram_Helpers:   
    
    hash_dict={}
        
    def __init__(self,samples):
        self.unigrams = self.loop(samples,1)
        self.bigrams = self.loop(samples,2)
        self.trigrams = self.loop(samples,3)
        self.total_words = sum(self.unigrams.values())
        
    def loop(self, samples, num):
        n_list = []    
        for s in samples:
            n_list = self.build_tweet(s, num)
            n_list = self.build_ngrams(n_list, num)
            self.hash_dict.update(self.count_gram(n_list, self.hash_dict))
        return self.hash_dict

    def build_tweet(self, s, num):
        tokenized = []
        for i in range(0, num - 1):
            tokenized += ["*"]
        tokenized += tok.tokenize(s)
        tokenized += ["~STOP~"]  
        return tokenized

    def build_ngrams(self, tokenized, num):
        hash_list = [] 
        for i in range(len(tokenized)-(num-1)):
    	    hash_gram = "_".join(tokenized[i:i+num])
            hash_list.append(hash_gram)
            print hash_list.count(hash_gram)
        return hash_list
        
    def count_gram(self, ngram_list, hash_gram):
        for gram in ngram_list:
            print gram
            hash_gram[gram] = hash_gram.get(gram, 0) + 1
            print hash_gram.get(gram)
        return hash_gram

    def pr_gram(self, r_gram_dict, string_input): #returns a list with counts of grams.
        count_list = []
        for i in string_input:
           if i in r_gram_dict:
              count = r_gram_dict.get(i)
              print count
           else:
              count = 0.0 # implement smoothing so we don't end up with div by zero
           count_list.append(count)
        return count_list

    def probability(self, count_3gram, count_2grams,count_1gram):
        feq = [self.get_ratio(x,y,z) for x, y, z in zip(count_3gram,count_2grams,count_1gram)]
        return reduce(operator.imul, feq)


    def get_ratio(self,x,y,z):
        p_3gram = 0
        p_2gram = 0
        p_1gram = 0
        if(y!=0):
            p_3gram = x/y
        if(z!=0):
            p_2gram = y/z
            p_1gram = z/self.total_words
        else:
            return 1.0/(2*self.total_words)
        return 0.8*p_3gram+0.15*p_2gram+0.05*p_1gram
            
class File_Utils:
    
    def crawl_directory(self,root_dir="~/Tweets"):
        file_group = []
        tweet_path = os.path.expanduser(root_dir)
        file_group = [f for f in os.listdir(tweet_path) if os.path.isfile(os.path.join(tweet_path, f))] 
        return file_group
     
    def create_samples(self, file_group,root_dir="~/Tweets"):
        samples = [] 
        tweet_path = os.path.expanduser(root_dir)
        for tweet_file in file_group:
            samples.extend(open(os.path.join(tweet_path, tweet_file)))
        for t in samples:
            print t
        return samples

###############################################################################
# up to 3grams must read output and output probability 
# the dog P(w2 | w1) the dog laughs P(w3 |w2, w1)
# P(w1|w-1, w0), * P(w2|w1, w0) symbols: stop and start anfor i ind replace -1 and end word etc with symbols
# p(the dog laughs) /p(the dog)

if __name__ == '__main__':
    tok = Tokenizer(preserve_case=False)
    fi = File_Utils()

    samples = []
    #file_group = fi.crawl_directory(root_dir="/Users/fdiacobe/research/git/interact/data/trainingData/lang_models")
    samples = fi.create_samples(["shakespeare.txt"],root_dir="/Users/fdiacobe/research/git/interact/data/trainingData/lang_models")
    n = NGram_Helpers(samples)

    line = raw_input('Enter a sentence:')
    line_copy = line
    input_three_list = n.build_tweet(line, 3)
    input_three_list = n.build_ngrams(input_three_list, 3)
    #print line_copy
    for x in input_three_list:
       print x
    
    input_two_list = n.build_tweet(line_copy, 2)
    input_two_list = n.build_ngrams(input_two_list, 2)
    #for l in input_two_list:
       #print l
       
    input_one_list = n.build_tweet(line_copy, 1)
    input_one_list = n.build_ngrams(input_one_list, 1)
    #for l in input_two_list:
       #print l

       
    count_3_list = n.pr_gram(n.trigrams, input_three_list)
    for k in count_3_list :
       print k
    count_2_list = n.pr_gram(n.bigrams, input_two_list)
    for f in count_2_list:
       print f
    
    count_1_list = n.pr_gram(n.unigrams, input_one_list)
    
    pr = n.probability(count_3_list, count_2_list,count_1_list)
    print pr

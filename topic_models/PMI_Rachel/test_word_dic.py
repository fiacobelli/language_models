from corpora import Corpora
import sys

if __name__=='__main__':
    word_dict = Corpora().deserialize_dict(sys.argv[1])
    q = raw_input("Query:")
    while len(q)>0:
        print word_dict.get(q,"Word Does Not exist")
        q = raw_input("Query:")


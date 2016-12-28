import pmi
import ngrams as ng

#ngrams = ng.__read_ngrams__("/Users/researchgroup/research/topic_model/data/wiki_ngram/wiki_modelmerge_1-10.dat")
ngrams = {}
print "done reading dict"
print pmi.__calculate_average_pmi__("/Users/researchgroup/research/topic_model/git/language_models/refine_topics/test_raw_topics/",ngrams)
print pmi.__calculate_average_pmi__("/Users/researchgroup/research/topic_model/git/language_models/refine_topics/test_ref_topics/",ngrams)

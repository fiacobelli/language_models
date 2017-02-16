import math
import numpy as np
import os
import deletedtopics as dt
import json
#get all raw files
#get directory to save refined raw
#for each raw file, get all pmis
#after getting pmi for all topics, calculate the sd and iterate through all topics again and keep only the ones that are good and save them to the firectotu
#once saved, send both raw and refined pmi and save their difference to a directory

 #then for each file get average pmi

raw_dir = "/Users/researchgroup/research/topic_model/data/raw_topics"
ref_dir = "/Users/researchgroup/research/topic_model/data/ref_topics"
del_dir = "/Users/researchgroup/research/topic_model/data/del_topics2/"
pmi_dir = "/Users/researchgroup/research/topic_model/data/results_pmi/refined_pmi_0215.csv"

pmidict = {}
files_in_dir = os.listdir(raw_dir)
for f in files_in_dir:
    pmi = []
    print "**", f
    if f.endswith('.txt'):
        with open(raw_dir + f) as file:
            for l in file:
                pmi.append(float(l.split(":")[1]))
        mean = np.mean(pmi)
        sd = np.std(pmi, ddof=1)
        max = mean + sd
        min = mean - sd
        print "pmi",pmi
        print "sd:",sd
        print "mean:",mean
        print "min max:", min,max
        refined_pmi = []
        refined_topics = ''
        with open(raw_dir + f) as file:
            for l in file:
                p = float(l.split(":")[1])
                if p >= min and p <=max:
                    refined_pmi.append(p)
                    refined_topics += l
        print "refined pmi",refined_pmi
        nf = open(ref_dir + f, "w")
        nf.write(refined_topics.strip("\n"))
        nf.close()
        parts = f.split("_")
        print parts
        name = parts[0]
        other = parts[2] + "_" + parts[3].split(".")[0]+ "_" + str(len(refined_pmi))
        if name in  pmidict:
            pmidict[name][other] = sum(refined_pmi)/len(refined_pmi)
        else:
             pmidict[name] = {other: sum(refined_pmi)/len(refined_pmi)}




      



#dump this to dictionary
json.dump(pmidict, open(pmi_dir, 'w'))
#get deleted topics
dt.getDiff(raw_dir, ref_dir, del_dir)
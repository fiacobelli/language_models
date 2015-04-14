'''
    This program takes pickled collections.Counters
    and blends them together.
'''
from collections import Counter
import cPickle
import sys, datetime

def merge(c1,c2):
    c1.update(c2)
    return c1


def merge_cf(c1,filen):
    c2 = file_to_counter(filen)
    return merge(c1,c2)

def merge_cf_dyn(c1,filen):
    with open(filen) as f:
        for line in f:
            if len(line)>2:
                key,val = line.split("\t")
                c1.update({key:int(val)})
    return c1

def file_to_counter_p(filen):
    f = open(filen,"rb")
    c = cPickle.load(f)
    f.close()
    return c


def file_to_counter(filen):
    counts = Counter()
    with open(filen) as f:
        for line in f:
            if len(line)>2:
                key,val = line.split("\t")
                counts[key]=int(val)
    return counts


def merge_files(flist):
    print "Reading ",flist[0]
    c = file_to_counter(flist[0])
    print len(c.keys()),"keys to merge"
    for f in flist[1:]:
        print datetime.datetime.now(),"Merging ",f
        c=merge_cf_dyn(c,f)
        print "So far:",len(c.keys()),"bigrams"
    return c

            
def write_counter(outfilename,counter):
    with  open(outfilename, "w") as testFile:
        for key,val in counter.items():
            if len(key)>0:
                 testFile.write("%s\t%s\n" % (key, val))


def write_counter_b(outfilename,counter):
    of = open(outfilename,"w")
    cPickle.dump(counter,of,cPickle.HIGHEST_PROTOCOL)
    of.close()


def merge_all(flist,ofile):
    print datetime.datetime.now(),"Merging files"
    c = merge_files(flist)
    print datetime.datetime.now(),"Saving file in plain text"
    write_counter(ofile,c)
    print datetime.datetime.now(),"Done"
    #print "Pickling counter binary form"
    #write_counter_b(ofile+".bin",c)


if __name__=="__main__":
   ofile = sys.argv[1]
   flist = sys.argv[2:]
   merge_all(flist,ofile)

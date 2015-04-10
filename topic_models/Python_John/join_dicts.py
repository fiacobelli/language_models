'''
    This program takes pickled collections.Counters
    and blends them together.
'''
from collections import Counter
import cPickle
import sys

def merge(c1,c2):
    c1.update(c2)
    return c1


def merge_cf(c1,filen):
    c2 = file_to_counter(filen)
    return merge(c1,c2)

def file_to_counter(filen):
    f = open(filen,"rb")
    c = cPickle.load(f)
    f.close()
    return c


def merge_files(flist):
    print "Reading ",flist[0]
    c = file_to_counter(flist[0])
    for f in flist[1:]:
        print "Merging ",f
        c=merge_cf(c,f)
        print "So far:",type(c),"bigrams"
    return c

def wordListPrinter(testList, testFile):
    for key,val in testList.items():
        if len(key)>0:
            testFile.write("%s\t%s\n" % (key, val))

            
def write_counter(outfilename,counter):
    testFile = open(outfilename, "w")
    #testFile.write(printHeader())
    wordListPrinter(counter, testFile)

def write_counter_b(outfilename,counter):
    of = open(outfilename,"w")
    cPickle.dump(counter,of,cPickle.HIGHEST_PROTOCOL)
    of.close()


def merge_all(flist,ofile):
    c = merge_files(flist)
    print "Saving file in plain text"
    write_counter(ofile,c)
    print "Pickling counter binary form"
    write_counter_b(ofile+".bin",c)


if __name__=="__main__":
   ofile = sys.argv[1]
   flist = sys.argv[2:]
   merge_all(flist,ofile)

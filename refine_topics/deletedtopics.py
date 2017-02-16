
import os

def read(f):
	with open(f, 'r') as myfile:
	    data=myfile.read()
	return data


def clean(s):
	return s[s.index(" ")+1: len(s)]


def diff(raw, refined):
	raw = raw.strip("\n")
	refined = refined.strip("\n")
	deleted_topics = ""
	c = 0
	for i in raw.split("\n"):
		rawtopic = clean(i)
		found = True
		for j in refined.split("\n"):
			reftopic = clean(j)
			if rawtopic == reftopic:
				found = False
		if found == True:
			deleted_topics += str(c) + " " + rawtopic + '\n'
			c+=1
	return deleted_topics




def getDiff(raw_dir, refined_dir, del_dir):
	for f in os.listdir(raw_dir):
		if f.endswith('.txt'):
			t = diff(read(raw_dir + f), read(refined_dir + f))
			nf = open(del_dir + f, "w")
			nf.write(t)




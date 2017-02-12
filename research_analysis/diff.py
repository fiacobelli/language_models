


def read(f):
	with open(f, 'r') as myfile:
	    data=myfile.read()
	return data


def clean(s):
	return s[s.index(" ")+1: len(s)]




raw = read('topics_raw')

refined = read('topics_refined')


for i in raw.split("\n"):
	rawtopic = clean(i)
	found = True
	for j in refined.split("\n"):
		reftopic = clean(j)
		if rawtopic == reftopic:
			found = False
	if found == True:
		print(rawtopic)


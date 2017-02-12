import csv
from scipy.stats import ttest_ind
import numpy as np


reader=csv.reader(open("data/reports/raw/pmi.csv" ,"rb"),delimiter=',')
raw_csv = list(reader)

reader = csv.reader(open("data/reports/refined/pmi.csv" ,"rb"),delimiter=',')
refined_csv = list(reader)


reader = csv.reader(open("data/reports/raw/ttest.csv" ,"rb"),delimiter=',')
raw_ttest = list(reader)


def list_pmis(genre, topic_count, topics_csv):
	pmis = []
	for i in range(1,len(topics_csv)):
		for j in range(1,len(topics_csv[i])):
			if topics_csv[0][j] == genre and str(topic_count) + "_" in topics_csv[i][0]:
				pmis.append(float(topics_csv[i][j]))
	return pmis


def ttest(a, b):
	print a
	print b
	return {
	"t": ttest_ind(a, b)[0],
	"p": ttest_ind(a, b)[1],
	"meanA": np.mean(np.subtract(a, b), axis=0),
	"meanB": 0,
	"sdA": np.std(np.subtract(a, b), axis=0),
	"sdB": 0,
	"df": len(a)-1 + len(b)-1,
	}

			
def export(f, arr):
	fl = open(f, 'w')

	writer = csv.writer(fl)

	for values in arr:
	    writer.writerow(values)

	fl.close()



ttest_detail = []
ttest_detail.append(["", "p", "t","df", "sd1", "sd2", "mean1", "mean2"])


for i in range(1, len(raw_ttest)):
	for j in range(1, len(raw_ttest[i])):		
		raw = list_pmis(raw_ttest[0][j], raw_ttest[i][0], raw_csv)
		refined = list_pmis(raw_ttest[0][j], raw_ttest[i][0], refined_csv)
		obj = ttest(raw, refined)
		if (obj["p"] < 0.05):
			raw_ttest[i][j] += " *"
		ttest_detail.append([raw_ttest[0][j] + " " + raw_ttest[i][0], obj["p"], obj["t"],obj["df"], obj["sdA"], obj["sdB"], obj["meanA"], obj["meanB"]]) 
		

export("data/reports/raw/ttest.csv", raw_ttest)
export("data/reports/compared_ttest_detailed.csv", ttest_detail)

		




 


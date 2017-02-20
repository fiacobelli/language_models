import csv
import numpy as np
from scipy.stats import ttest_ind


pmi_csv_path = "data/reports/refined_pmi.csv"
report_path = "data/reports/refined_report.txt"



def getArray(row, col):
	newArr = []
	for i in range(row,row + 10):
		newArr.append(x[i][col])
	return newArr


def getTtest(a, b, corpA, corpB):
	t = ttest_ind(a, b)[0]
	p = ttest_ind(a, b)[1]
	meanA = np.mean(a, axis=0)
	meanB = np.mean(b, axis=0)
	sdA = np.std(a, axis=0)
	sdB = np.std(b, axis=0)
	df = len(a)-1 + len(b)-1
	#Using Latent Dirichilet Allocation, the PMI for the Senate corpora with 30 topics was significantly higher than the Essay corpora with 30 topics (t = 21.3296, p < 0.0001)
	
	sig = "not a significant"
	if (p < 0.05):
		sig = "a significant"

	with open(report_path, "a") as f:
		f.write("There was " + sig + " difference between the PMI values of the " + corpA + " corpora (M=" + str(meanA) + ", SD=" + str(sdA) +") and the " + corpB + " corpora (M=" + str(meanB) + ", SD=" + str(sdB) + "); t (" + str(df) + ")=" + str(t) + ", p = " +str(p) + "\n\n\n")





reader=csv.reader(open(pmi_csv_path ,"rb"),delimiter=',')
x=list(reader)


#ttesting all topic num pmis

for i in range(2, len(x), 11):
	
	senate = [float(k) for k in getArray(i, 1)]
	essays = [float(k) for k in getArray(i, 2)]
	nytimes = [float(k) for k in getArray(i, 3)]

	topic_num = "_" +x[i-1][0]

	#compare senate and essays
	getTtest(senate, essays, "Senate" + topic_num, "Essays" + topic_num)
	#compare senate and nytimes
	getTtest(senate, nytimes, "Senate" + topic_num, "NyTimes" + topic_num)
	#compare essays and nytimes
	getTtest(essays, nytimes, "Essays" + topic_num, "NyTimes" + topic_num)
	
	


#ttesting the averages of each corpora only
senate = []
essays = []
nytimes =[]
for i in range(1, len(x) -1 , 11):
	senate.append(float(x[i][1]))
	essays.append(float(x[i][2]))
	nytimes.append(float(x[i][3]))	

#compare senate and essays
getTtest(senate, essays, "Senate" , "Essays" )
#compare senate and nytimes
getTtest(senate, nytimes, "Senate", "NyTimes")
#compare essays and nytimes
getTtest(essays, nytimes, "Essays", "NyTimes")

	
'''   FORMAT
Topics	senate	essays	nytimes	
30	2.1131213959906106	1.6273230858115273	1.9934929074074001	
30_1	2.0799646726566787	1.6423521833914685	2.0281004211144285	
30_2	2.0907723483226843	1.6052251679864595	1.985448506430523	
30_3	2.1225703031392666	1.6774567653911454	2.0416404302287545	
30_4	2.1117544885467483	1.6602978689123586	2.0315606054634494	
30_5	2.0865874306050602	1.6165686012260252	1.9640181768174734	
30_6	2.0821781634793637	1.5520052418276247	2.0414724721516473	
30_7	2.1281793757661998	1.5292380554867089	1.9554249442635696	
30_8	2.116449994660276	1.620972534813015	1.9441597000784463	
30_9	2.221663924317381	1.6370479280272432	1.974725447761848	
30_10	2.091093258412448	1.7320665110532258	1.9683783697638602	'''


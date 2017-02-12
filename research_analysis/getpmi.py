import json
import csv
from pprint import pprint
from scipy.stats import ttest_ind
import numpy as np

type = "raw"

def createArray(row, col):
	return [[None for i in range(col)] for j in range(row)]


def initializeTopicsCsv(arr):
	with open('data/' + type + '_pmi.txt') as data_file:
		data = json.load(data_file)
	topics = []
	files = [30, 50, 100, 200, 400] #**change
	for f in files:
		for i in range(0,11): #**change
			if i == 0:
				topics.append(str(f))
			else:
				topics.append(str(f) + '_' + str(i))

	#adding topic label columns to csv array
	for i in range(0, len(topics)):
		arr[i + 1][0] = topics[i]

	#reading file and setting values to array
	arr[0][0] = 'Topics'
	
	arr[len(arr) -1 ][0] = 'Average'


	i = 2
	#adding genre labels 
	for genre in data:
		arr[0][i -1] = 'Actual Topics'
		arr[0][i] = str(genre)
		for topic in data[genre]:
			parts = str(topic).split("_")
			t = parts[0]
			if (len(parts) > 1):
				t += "_" + parts[1]
			if len(parts) > 2:
				arr[topics.index(t) + 1][i-1] = parts[2]
			arr[topics.index(t) + 1][i] = data[genre][topic]
		
		
		sm = 0 #get average for all files of a genre
		for t in topics:
			sm += arr[topics.index(str(t)) + 1][i]
		arr[len(arr) -1 ][i] = sm/len(topics)
		i += 2

	#get average of each file type
	return arr


def exportCsv(arr, f):
	fl = open(f, 'w')

	writer = csv.writer(fl)

	for values in arr:
	    writer.writerow(values)

	fl.close()



def initializeTopicsTtestCsv(topics_csv, topics_ttest_csv):
	topics_ttest_csv[0][0] = "Topics"
	
	#getting labels senate, essays,ny
	k = 1
	for j,l in enumerate(topics_csv[0][1:]):
		if j%2 == 1:
			topics_ttest_csv[0][k] = l  
			k += 1
	i = 1
	for t in topics_csv[1:len(topics_csv)-1]:
		if "_" not in t[0]:
			topics_ttest_csv[i][0] = t[0]
			k = 1
			#populating the pmi for each topic count of all genres
			for j,l in enumerate(t[1:]):
				if j%2 == 1:
					topics_ttest_csv[i][k] = l 
					k += 1
			i += 1
	return topics_ttest_csv

def ttest(topics_csv, topics_ttest_csv):
	i = 1
	for i in range(i,len(topics_ttest_csv)):
		j = 1
		for j in range(j,len(topics_ttest_csv[i])):
			next_i = i+1
			next_j = j+1			
			if next_i >= len(topics_ttest_csv):
				next_i = 1
			if next_j >= len(topics_ttest_csv[i]):
				next_j = 1

			mainGenre = topics_ttest_csv[0][j]
			mainTopic = topics_ttest_csv[i][0]
			main = list_pmis(mainGenre, mainTopic, topics_csv)


			rightGenre = topics_ttest_csv[0][next_j]
			rightTopic = topics_ttest_csv[i][0]
			right = list_pmis(rightGenre, rightTopic, topics_csv)
			obj = dottest(main, right)
			p = obj["p"]
			topics_ttest_detailed.append([mainGenre + " " + mainTopic + " vs " + rightGenre + " " + rightTopic, obj["p"], obj["t"],obj["df"], obj["sdA"], obj["sdB"], obj["meanA"], obj["meanB"]])
			
			if p < 0.05:
				if clean(topics_ttest_csv[i][j]) < clean(topics_ttest_csv[i][next_j]):
					topics_ttest_csv[i][j] = str(topics_ttest_csv[i][j]) + " <"
				else:
					topics_ttest_csv[i][j] = str(topics_ttest_csv[i][j]) + " >"
			else:
				topics_ttest_csv[i][j] = str(topics_ttest_csv[i][j]) + " -"	



			bottomGenre = topics_ttest_csv[0][j]
			bottomTopic = topics_ttest_csv[next_i][0]
			bottom = list_pmis(bottomGenre, bottomTopic, topics_csv)
			obj = dottest(main, bottom)
			p = obj["p"]
			topics_ttest_detailed.append([mainGenre + " " + mainTopic + " vs " + bottomGenre + " " + bottomTopic, obj["p"], obj["t"],obj["df"], obj["sdA"], obj["sdB"], obj["meanA"], obj["meanB"]])
			if p < 0.05:
				if clean(topics_ttest_csv[i][j]) < clean(topics_ttest_csv[next_i][j]):
					topics_ttest_csv[i][j] = str(topics_ttest_csv[i][j]) + " ^"
				else:
					topics_ttest_csv[i][j] = str(topics_ttest_csv[i][j]) + " V"
			else:
				topics_ttest_csv[i][j] = str(topics_ttest_csv[i][j]) + " -"
	return topics_ttest_csv


			#doing the actual ttest
			

def clean(s):
	return float(str(s).replace("V", "").replace("^","").replace("<","").replace(">","").replace("-","").replace(" ",""))

def formatTtest(obj):
	return "p:",obj["p"],"t(",obj["df"],"):",obj["t"],"meanA:",obj["meanA"],"meanB:",obj["meanB"],"sdA:",obj["sdA"],"sdB", obj["sdB"]


def dottest(a, b):
	return {
	"t": ttest_ind(a, b)[0],
	"p": ttest_ind(a, b)[1],
	"meanA": np.mean(a, axis=0),
	"meanB": np.mean(b, axis=0),
	"sdA": np.std(a, axis=0),
	"sdB": np.std(b, axis=0),
	"df": len(a)-1 + len(b)-1,
	}

			


def list_pmis(genre, topic_count, topics_csv):
	pmis = []
	for i in range(1,len(topics_csv)):
		for j in range(1,len(topics_csv[i])):
			if topics_csv[0][j] == genre and str(topic_count) + "_" in topics_csv[i][0]:
				pmis.append(topics_csv[i][j])
	return pmis



def initializeTopicsReduction(topics_csv, topics_red_csv):
	topics_red_csv[0][0] = "Topics"
	#getting labels senate, essays,ny
	k = 1
	for j,l in enumerate(topics_csv[0][1:]):
		if j%2 == 1:
			topics_red_csv[0][k] = l  
			k += 1
	i = 1
	for r,t in enumerate(topics_csv[1:len(topics_csv)-1]):
		if "_" not in t[0]:
			topics_red_csv[i][0] = t[0]
			k = 0
			n = 1
			for l in t:
				num = []
				if k%2 != 0:
					for m in range(r+2, r+2+10):
						num.append(topics_csv[m][k]) #change
					topics_red_csv[i][n] = int(round(sum([float(p) for p in num])/len(num)))
					n += 1
				k += 1
			i += 1

	exportCsv(topics_ttest_detailed, "data/reports/" + type + "/ttest_detailed.csv")		
	return topics_red_csv

#number of different types of topic size for each genre -> 30,50,100,200,400
topic_count = 5
#number of iterations for each topic size
iter_count = 11
#topics, senate, essays etc
header = 1
#average of total genre
footer = 1
#where the topics num is written
sidebar = 1
#senate essays, ny
genre_count = 3

row = iter_count * topic_count + footer + header
col = sidebar + 2 * genre_count # *2 the actual number of topics beside each file pmi
topic_csv = createArray(row, col)
topic_csv = initializeTopicsCsv(topic_csv)
exportCsv(topic_csv, "data/reports/" + type + "/pmi.csv")



#topics_ttest_csv
row = topic_count + header
col = genre_count + sidebar
topics_ttest_csv = createArray(row, col)

row = genre_count * topic_count + footer
col = 7 + sidebar #p, t, sdA, sdB, meanA, meanB, df
topics_ttest_detailed = []
mai = ["", "p", "t","df", "sd1", "sd2", "mean1", "mean2"]
topics_ttest_detailed.append(mai)

topics_ttest_csv = initializeTopicsTtestCsv(topic_csv, topics_ttest_csv)
topics_ttest_csv = ttest(topic_csv, topics_ttest_csv)
exportCsv(topics_ttest_csv, "data/reports/" + type + "/ttest.csv")


#topics_ttest_detailed


#topics_count_reduction

topics_red_csv = createArray(row, col)
topics_red_csv = initializeTopicsReduction(topic_csv, topics_red_csv)
exportCsv(topics_red_csv, "data/reports/" + type + "/topic_count.csv")




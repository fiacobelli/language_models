import math;
import pprint;
import sys;
import csv;
sys.path.insert(0, 'Code/')
import stats as st;
import topic_model as tm;
import kullback as kb;
import matplotlib.pyplot as plt
import os
import argparse

#takes in an array and decides which [topic1][topic2] has a kb less than normal kb of all values
#
def getTrashTopics(divergence,min_norm):
	trash_topics = [];
	for i, topic_div in enumerate(divergence):
		if (topic_div < min_norm):
			trash_topics.append(str(i)+' '+str(topic_div));
	return trash_topics;

def graphUniformTopic(topic,uniform):
	plt.plot(range(len(words)), topic);
	plt.plot(range(len(words)), uniform);
	plt.show();

def displayStats(sd,mean,min,kb):
	print "Standard Deviation: "+ str(sd);
	print "Mean: "+ str(mean);
	print "Min Normal: "+ str(min);
	print "KB Value: "+ str(kb);	

args = argparse.ArgumentParser("Finds garbage topics by comparing to a uniform distribution")
args.add_argument("f",help="File with the count of words in a topic")
args.add_argument("n",help="Number of topics")
args.add_argument("p",help="probability of words to be considered in finding the uniform topic")
args.add_argument("a",help="Enter 1 for saving topics, 2 for showing garbage topics, 3 graphic a topic against a uniform topic")

if __name__ == "__main__":
	values=args.parse_args()
	file_name =  values.f
	topic_num = int(values.n);
	perc = int(values.p);
	choice = int(values.a);
	#print ('\n');
	#perc = input("Enter Percentage for Uniform Topics: ");
	#print ('\n');
	#print "Getting topics....";

	topics = tm.getTopics(file_name,topic_num,2);
	words = tm.getWords(topics);

	#print "Calculating KB Divergence of all topics against uniform topic....";
	garbage_prob_topics = tm.getUniformTopic(topics, perc/100.0);
	garbage_kb = kb.getUniformTopicKb(topics,garbage_prob_topics);

	#print "Finding all trash topics and their KB divergence....";
	garbage_sd = st.getStandardDeviation(garbage_kb);
	garbage_mean = st.getMean(garbage_kb);
	garbage_min_norm = garbage_mean - (garbage_sd);
	garbage_topics = getTrashTopics(garbage_kb,garbage_min_norm);


	if (choice == 1):
		hn

	elif (choice == 2):
		pprint.pprint(garbage_topics);

	elif (choice == 3):		
		t_index = input("Enter a Topic number 0-"+str(topic_num-1)+": ");
		st.display(garbage_sd,garbage_mean,garbage_min_norm,garbage_kb[t_index])
		topic = tm.getTopicGraph(topics,t_index);
		graphUniformTopic(topic,garbage_prob_topics[t_index]);

	else:
		print "Invalid Choice!!";
		cont = False;

	#print "Ready!!";

	#cont = True;
	#while (cont):

		#print ('\n');
		#print ("Enter ....");
		#print ("1. Save Topics as a File.");
		#print ("2. Get list of Trash topics and their kb values.");
		#rint ("3. Graph trash topic against a uniform topic.");

		#print ('\n');

	
		#choice = input("Enter Choice: ");
		#print ('\n');







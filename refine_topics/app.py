import math;
import pprint;
import sys;
import csv;
sys.path.insert(0, 'Code/')
import stats as st;
import topic_model as tm;
import kullback as kb;
import matplotlib.pyplot as plt


#takes in an array and decides which [topic1][topic2] has a kb less than normal kb of all values
def getSimilarTopics(divergence,min_norm):
	similar_topics = [];
	for i, topics in enumerate(divergence):	
		for j, topic_div in enumerate(topics[i+1:]):
			if (topic_div < min_norm):
				similar_topics.append(str(i)+' '+str(j+1+i)+ ' '+str(topic_div));
	return similar_topics;


def getTrashTopics(divergence,min_norm):
	trash_topics = [];
	for i, topic_div in enumerate(divergence):
		if (topic_div < min_norm):
			trash_topics.append(str(i)+' '+str(topic_div));
	return trash_topics;


def saveTopic(topics, name, topic_num):
	fl = open("Files/Topics_csv/"+name, 'w')
	writer = csv.writer(fl)
	writer.writerow(["Words"]+range(topic_num));
	for values in topics:
		writer.writerow(values)
	fl.close();  

def graphTwoTopics(topics, index1, index2):
	t2 = tm.getTopicGraph(topics,index1);
	plt.plot(range(len(words)), t2);
	t2 = tm.getTopicGraph(topics,index2);
	plt.plot(range(len(words)), t2);
	plt.show();

def graphUniformTopic(topics,index):
	t2 = tm.getTopicGraph(topics,index);
	plt.plot(range(len(words)), t2);
	t2 = tm.getUniformTopic(topics);
	plt.plot(range(len(words)), t2);
	plt.show();

def displayStats(sd,mean,min,kb):
	print "Standard Deviation: "+ str(sd);
	print "Mean: "+ str(mean);
	print "Min Normal: "+ str(min);
	print "KB Value: "+ str(kb);	

if __name__ == "__main__":

	file_name =  sys.argv[1];
	topic_num = int(sys.argv[2]);	
	print "Getting topics....";

	topics = tm.getTopics(file_name,topic_num);
	words = tm.getWords(topics);

	print "Calculating KB Divergence of all topics in cross product....";
	similar_kb= kb.getAllTopicKb(topics);

	print "Finding all pairs of similar topics and their KB divergence....";
	similar_sd = st.getStandardDeviation(similar_kb);
	similar_mean = st.getMean(similar_kb);
	similar_min_norm = similar_mean - similar_sd;
	similar_topics = getSimilarTopics(similar_kb,similar_min_norm);


	print "Calculating KB Divergence of all topics against uniform topic....";
	garbage_kb = kb.getUniformTopicKb(topics);

	print "Finding all trash topics and their KB divergence....";
	garbage_sd = st.getStandardDeviation(garbage_kb);
	garbage_mean = st.getMean(garbage_kb);
	garbage_min_norm = garbage_mean - garbage_sd;
	garbage_topics = getTrashTopics(garbage_kb,garbage_min_norm);


	print "Ready!!";

	cont = True;
	while (cont):

		print ('\n');
		print ("Enter ....");
		print ("1. Save Topics as a File.");
		print ("2. Get list of similar topics and their kb values.");
		print ("3. Graph 2 similar topics.");
		print ("4. Get list of Trash topics and their kb values.");
		print ("5. Graph trash topic against a uniform topic.");

		print ('\n');

	
		choice = input("Enter Choice: ");
		print ('\n');


		if (choice == 1):
			name = raw_input("Save File as: ");
			saveTopic(topics, name, topic_num);
			print "Saved!";

		if (choice == 2):
			pprint.pprint(similar_topics);

		if (choice == 3):
			t_index1 = input("Enter First Topic number 0-"+str(topic_num-1)+": ");
			t_index2 = input("Enter Second Topic number 0-"+str(topic_num-1)+": ");
			displayStats(similar_sd,similar_mean,similar_min_norm,similar_kb[t_index1][t_index2]);
			graphTwoTopics(topics, t_index1 , t_index2);

		if (choice == 4):
			pprint.pprint(garbage_topics);

		if (choice == 5):		
			t_index = input("Enter a Topic number 0-"+str(topic_num-1)+": ");
			displayStats(garbage_sd,garbage_mean,garbage_min_norm,garbage_kb[t_index]);	
			graphUniformTopic(topics,t_index);

		print ('\n');
		cont = raw_input("Continue: (y/n): ");
		if cont == "n":
			cont = False;





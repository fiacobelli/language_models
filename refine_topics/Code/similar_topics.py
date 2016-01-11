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


def graphTopics(topics, index1, index2):
	t2 = tm.getTopicGraph(topics,index1);
	plt.plot(range(len(words)), t2);
	t2 = tm.getTopicGraph(topics,index2);
	plt.plot(range(len(words)), t2);
	plt.show();


if __name__ == "__main__":

	file_name =  sys.argv[1];
	topic_num = int(sys.argv[2]);	
	print "Getting topics....";

	topics = tm.getTopics(file_name,topic_num,2);
	words = tm.getWords(topics);

	print "Calculating KB Divergence of all topics in cross product....";
	similar_kb= kb.getAllTopicKb(topics);

	print "Finding all pairs of similar topics and their KB divergence....";
	similar_sd = st.getStandardDeviation(similar_kb);
	similar_mean = st.getMean(similar_kb);
	similar_min_norm = similar_mean -  similar_sd;
	similar_topics = getSimilarTopics(similar_kb,similar_min_norm);


	print "Ready!!";

	cont = True;
	while (cont):

		print ('\n');
		print ("Enter ....");
		print ("1. Save Topics as a File.");
		print ("2. Get list of similar topics and their kb values.");
		print ("3. Graph 2 similar topics.");

		print ('\n');

	
		choice = input("Enter Choice: ");
		print ('\n');


		if (choice == 1):
			name = raw_input("Save File as: ");
			tm.save(topics, name, topic_num);
			print "Saved!";

		if (choice == 2):
			pprint.pprint(similar_topics);

		if (choice == 3):
			t_index1 = input("Enter First Topic number 0-"+str(topic_num-1)+": ");
			t_index2 = input("Enter Second Topic number 0-"+str(topic_num-1)+": ");
			st.display(similar_sd,similar_mean,similar_min_norm,similar_kb[t_index1][t_index2]);
			graphTopics(topics, t_index1 , t_index2);

		if (choice == 0):
			print "Bye!";
			cont = False;





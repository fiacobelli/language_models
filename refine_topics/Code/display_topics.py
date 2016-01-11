import math;
import pprint;
import sys;
import csv;
sys.path.insert(0, 'Code/')
import stats as st;
import topic_model as tm;
	

def displayTopic(topics):
	topics = zip(*topics);
	words = [x for (y,x) in sorted(zip(topics[1],topics[0]),reverse=True)];
	prob = sorted(topics[1],reverse=True);
	return zip(words,prob)[:12];

def displayTopics(topics):
	topics = zip(*topics);
	for i,topic in enumerate(topics[1:]):
		words = [x for (y,x) in sorted(zip(topic,topics[0]),reverse=True)];
		print str(i)+' '+(', '.join(words[:12]));



if __name__ == "__main__":

	file_name =  sys.argv[1];
	topic_num = int(sys.argv[2]);	
	choice = int(sys.argv[3]);

	topics = tm.getTopics(file_name,topic_num,2);
	words = tm.getWords(topics);
	if (choice == 1):
		f = os.path.basename(file_name)
		tm.save(topics, f[:-3]+"csv", topic_num)
		print "Saved!";

	if (choice == 2):
		displayTopics(topics);

	if (choice == 0):
		print "Invalid Choice!";
		cont = False;

	#cont = True;
	#while (cont):

		#print ('\n');
		#print ("Enter ....");
		#print ("1. Save Topics as a File.");
		#print ("2. Display topics.");

		#print ('\n');

	
		#choice = input("Enter Choice: ");
		#print ('\n');


		





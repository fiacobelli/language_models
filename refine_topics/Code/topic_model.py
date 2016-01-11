# PUBLIC creates a 2d array of topics as columns and words as arrays. a topic[index] will give a word actually and its probability
import csv
def getTopics(filename, topic_num, prob_choice):
	topics = []
	words = 0;
	with open(filename) as f:	
	    for line in f: 
	    	words = words+1;   	
	    	parts = line.split();
	    	if len(parts) > 2:
	    		topics.append(getWordRow(parts, topic_num));
	    if(prob_choice == 1):
	    	return getTopicsWordOverTopics(topics);
	    elif(prob_choice == 2):
	    	return getTopicsWordOverWords(topics);
	    else:
	    	return getTopicsWordOverDocument(topics,words);

	    

#takes the word and puts it into assigned topics and returns a row of word and the times it occurs
def getWordRow(parts, topic_num):
	word_row = [0] * (topic_num + 1); 
	word_row[0] = parts[1];#the word
	for weight in parts[2:]:#the topics it occurs in
		word_index = int (weight.split(':')[0]) +1;
		word_weight = float (weight.split(':')[1]);
		word_row[word_index] = word_weight;
	return word_row;

#word topic1 topic 2
#changes each row of word in the 2d array from times it occurs (x) to probabilities by dividing x/sum of the x in the whole row
#the probability of the word to be in this topic from all topics
def getTopicsWordOverTopics(topics):
	topic_prob = []
	for word_row in topics:
		total_weight = sum(word_row[1:]);
		topic_prob.append([word_row[0]]+[float(x)/total_weight for x in word_row[1:]]);
	return topic_prob;

# PUBLIC returns a topic with its probabilities 
def getTopicGraph(topics, index):
	topic = zip(*topics);
	return topic[index+1]

#
def getUniformTopic(topics, perc):
	uniform_topics=[];
	topics = zip(*topics);
	for topic in topics[1:]:
		sorted_topic = sorted(topic, reverse = True)	
		size = total = prev = 0
		for p in sorted_topic:
			if (p!= prev):
				if (total >= perc or p == 0):
					break;
				else:
					total = float(total) + p;
			prev = p;
			size = size + 1;

		uniform_prob = 1.0/size; #len gives number of words
		uniform_topics.append([uniform_prob for i in topic]);
	return uniform_topics;


#gets the listof words	
def getWords(topics):
	topic = zip(*topics);
	return topic[0];



def save(topics, name, topic_num):
	fl = open("../Files/Topics_csv/"+name, 'w')
	writer = csv.writer(fl)
	writer.writerow(["Words"]+range(topic_num));
	for values in topics:
		writer.writerow(values)
	fl.close();  

#the probability of the word being in this topic from all of the words in the topic
def getTopicsWordOverWords(topics):
	#topics word1 word2
	topic_prob = []
	topics = zip(*topics);
	topic_prob.append(topics[0]);
	for topic in topics[1:]:
		total_weight = sum(topic);
		topic_prob.append([float(x)/total_weight for x in topic]);
	return zip(*topic_prob);


def getTopicsWordOverDocument(topics,total_words):
	#topics word1 word2
	topic_prob = []
	topics = zip(*topics);
	topic_prob.append(topics[0]);
	for topic in topics[1:]:
		topic_prob.append([float(x)/total_words for x in topic]);
	return zip(*topic_prob);



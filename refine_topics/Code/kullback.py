import math;

# PUBLIC KB value for all topics mapped to all other topics . Returns a 2D array
def getKbDivergence(topic_a, topic_b):
	divergence = 0;
	for p1,p2 in map(None,topic_a,topic_b):
		if (p1 > 0 and p2 > 0):
			divergence = divergence + p1 * math.log(p1/p2);
	return divergence


# PUBLIC gets KB value for all topics mapped to all other topics in 2D array
def getAllTopicKb(topics):
	topics = zip(*topics);
	topic_num = len(topics) - 1; #len of topics
	kb_divergence= [[0 for i in range(topic_num)] for j in range(topic_num)];
	i = 0;
	for topic_a in topics[1:]:
		j=i+1;
		for topic_b in topics[j+1:]:
			kb_divergence[i][j] = getKbDivergence(topic_a,topic_b);
			j = j+1;
		i=i+1;
	return kb_divergence;


def getUniformTopicKb(topics, uniform_topic):
	kb_divergence = [];
	topics = zip(*topics);
	for i,topic in enumerate(topics[1:]):
		kb_divergence.append(getKbDivergence(topic,uniform_topic[i]));
	return kb_divergence;




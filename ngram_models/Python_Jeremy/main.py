import re, os, math
from NGram import NGram

# configuration 
dictionarySource = "dictionary.txt"
URLSuffixesFile = "url_suffixes.txt"
maxNGramSize = 3

# define objects
dictionary = {}
nGramGroups = []

# define constants
START = "@START@";
END = "@END@";
SEPARATOR = "@SEP@";

# define regular expressions

# WORDS
wordsRegex = r"""
	# word match
	(?=
		# pre-word match
		(?:
			\s										# beginning space
			[\(\[\{]*								# beginning brackets
			(?:\'?\"?|\"?\'?)?						# beginning quotes
		)
		
		# base word match
		(?:
			[a-zA-Z]|								# letter-only
			[a-zA-Z]-|								# hyphenated
			[a-zA-Z]'								# apostrophes allowed
		)+
		(?<=[a-zA-Z])								# always end a base word with a letter
		
		# post-word match
		(?:							
			[:;,]?|	  								# clause terminators	
			(?:[\.?!]+)?							# sentence terminators
		)?
		(?:\'?\"?|\"?\'?)?							# ending quotes
		[\)\]\}]*									# ending brackets
		(?:
			[:;,]?|		  							# clause terminators // not followed by other terminators
			(?:[-\.?!]+)?							# sentence terminators // may be followed by other terminators
		)?
		\s											# end with space (end of word)
    )
	(?:\s+)												# consume at least one space
	(?:[^-'a-zA-Z]*)									# consume all other non base-word characters
	# base word group
	(	
		#(?![-']{2,})			  					# limit on inner word punctuation
		[-'a-zA-Z]+
		\b
	)
	
	# space match
	#(?=
	#(\s+)
	#)
	#(\s+)
	# punctuation match
	#(?![a-zA-Z]
	#[?]+|[!]+|[.]+|[,]+
	"""
	
# URLs
URLSuffixes = []
for line in open(URLSuffixesFile):
	line = line.strip('\n')
	if(line.isalpha() and (not line.startswith("//") and line != "")):
		URLSuffixes.append(line.strip(''))
URLSuffixes = '|'.join(URLSuffixes[:-1]).replace(".", "\.")
print URLSuffixes

urlRegex = r"""
	(?:
		(?=
			(?:https?:\/\/)? # protocol
			(?:[a-zA-Z\d\.-]+) # domain
			\.
			(?:("""+URLSuffixes+""")) #(?:[a-zA-Z\.]{2,6}) # tld
			(?:[\/\w\.-]*)* # file structure
			\/?  # trailing slash
		)
	)
	\S*
	"""
urlRegex = re.compile(urlRegex, re.VERBOSE)

# EMOTICONS
emoticonsRegex = r"""
	(?:
		(?=
		
				# FACES
				# horizontal
					# left-to-right faces
		[|>]*				# top
		[:;=XxB|#%8]		# eyes
		'*				# tears
		[-^\?]?				# nose
		[\.,LS$@\(\)\[\]\{\}xX0OoD3Dc\<\>\/\\\|pP]+			# mouth
						# bottom
					# right-to-left faces
				# vertical
			# symbols ???
		\s # word end
		)
	)
	\S*
"""
emoticonsRegex = re.compile(emoticonsRegex, re.VERBOSE)
	
# HASHTAGS
hashtags = "some stuff #hash-tag good"
hashtagRegex = r"""
	(?=
		(?:
			\#
			\w+
		)
	)
	\S*
"""
hashtagRegex = re.compile(hashtagRegex, re.VERBOSE)	
	
# Generate dictionary
# Hashtable<NGram, Integer>[]
def generateDictionary():	
	# globals
	global nGramGroups, dictionarySource
	
	print("\nGenerating dictionary from sources folder...\n")
	
	# loop through all files in sources folder
	for source in os.walk("sources"):	
		sourceText = ""
		sourceText += ' '.join([line.strip() for line in open(source[0] + "\\" + source[2][0])])
		
		# extract NGrams from file and store them
		print("Fetching n-grams from file: " + str(source[2][0]) + "\n")
		
		num = extract(sourceText, maxNGramSize)
		
		print("Added " + str(num) + " entries to the dictionary.")
		
		# write nGramGroups to file
		file = open(dictionarySource, "w")
		for group in nGramGroups: # For each of the Hashtables
			for nGram, count in group.items(): # For each NGram
				file.write(str(nGram) + "\t" + str(count) + "\n") # write entries to new line
				#print(str(nGram) + "\t" + str(count)) # print nGram to console
		file.close();
		print ("\nSaved to " + dictionarySource + "...")
			
		#return nGramGroups;

# Extract NGrams from text
def extract(source, n):		
	#globals
	global nGramGroups
	
	# init nGramGroups
	for i in range(n):
		nGramGroups.append(dict())
	
	# init count to 0
	count = 0
	
	# Output filter source
	source = applyFilters(source)
	
	# Log filtered source
	#file = open("filteredsource.txt", "a")
	#file.write(source)
	#file.close()
	
	# Split source into multiple words
	words = source.split(" ")

	# Loop through words[]
	for i in xrange(0, len(words)):
	
		# Loop through nGramGroups
		# for nGrams of size {1, ... n-1, n}
		for m in xrange(1, n+1): # Loop from 1 to n

			# Fetch current nGramGroup
			nGramGroup = nGramGroups[m-1]
			
			# Create a new NGram of size m+1
			nGram = NGram(m)
			
			# Add words to the nGram
			for w in xrange(1-m, 1): # Loop from 1-m to 0
				if i+w >= 0:
					nGram.addWord(words[i+w])
				else:
					nGram.addWord(SEPARATOR)
					
			#print("Added " + str(nGram))
	
			# Record NGram
			if nGram in nGramGroup: # if nGram exists in this nGramGroup
				nGramGroup[nGram] = nGramGroup[nGram] + 1 # Increment NGram's count
				#print("incrementing dict entry")
				
			else: # else nGram is new
				nGramGroup[nGram] = 1 # Add new NGrams to nGramGroup
				count = count + 1 # Increment count
				#print("adding dict entry")
				
			
		
	return count # Return the number of entries added to the dictionary

# Loads dictionary from dictionary.txt
def loadDictionary():
	# globals
	global dictionary, dictionarySource
	
	# parse dictionary source
	for line in open(dictionarySource):
		line = line.strip();
		parts = re.split(r'\s+', line)
		key = ' '.join(parts[1:-1])
		val = parts[-1]
		dictionary[key] = val

def count1Grams(): 
	# globals
	global dictionary
	
	count = 0
	for gram in dictionary:
		if(len(gram.split(' ')) == 1):
			count = count + 1
	return count
	
def getProb(inputString, n):
	
	# declarations
	product = 1 # set initial product to 1
	words = inputString.strip().split(' ')	# store words in list
	
	# make sure: 1 <= n <= len(words)
	n = max(1, min(len(words), n))
	
	# loop through words
	for i in range(0, len(words)-n+1):
		
		# collect a new nGram of words from the current position
		nGram = []
		
		# at the current position, loop through a set of n words
		for j in range(i, i+n):
			nGram.append(words[j])
				
		# get counts
		a = ' '.join(nGram) # join words
		a = int(getCount(a)) # return count
		b = ' '.join(nGram[0:-1]) # join words
		b = int(getCount(b)) #return count

		if(b != 0):
			product = 1.0 * product * a/b # append product
		else:
			product = 0;
		
	# return probability
	return product
	
def getCount(key):
	global dictionary
	if key in dictionary:
		return dictionary[key]
	elif not key: # if string is empty
		return count1Grams() # return number of 1-GRAMS
	else: return 0

def getPerp():
	global maxNGramSize
	# loop through all files in sources folder
	sentences = []
	for source in os.walk("sources"):
		sourceText = ""
		sourceText += ' '.join([line.strip() for line in open(source[0] + "\\" + source[2][0])])
		sourceText = applyFilters(sourceText)
		sentences.extend(sourceText.split("@sep@"))
		
	sum = 0
	m = len(sentences)
	
	for i in range(0, m):
		pr = getProb(sentences[i], maxNGramSize)
		pr = pr if pr!=0 else 0
		sum = sum + pr
	return math.pow(2, (1.0/m * sum * -1))
	
def applyFilters(source):

	# tag URLs
	source = re.sub(urlRegex, r"@URL@", source)
	
	# tag EMOTICONS
	source = re.sub(emoticonsRegex, r"@EMO@", source)
	
	# tag HASHTAGS
	source = re.sub(hashtagRegex, r"@HASH@", source)
	
	# Collapse unnecessary whitespace
	source = re.sub(r"[\s\t]{2,}", " ", source)
	
	# Put SEPARATOR at beginning and ending of source
	source = SEPARATOR + " " + source.strip() + " " + SEPARATOR
	
	# Put SEPARATOR after terminating punctuation
	source = re.sub(r"([\?\!\.]+)", r"\1 " + SEPARATOR, source)

	# make LOWERCASE
	source = source.lower()
		
	#Put spaces around punctuation
	source = re.sub(r"[\s]*([\-\:\,\?\!\.]+)[\s]*", r" \1 ", source)
		
	#print("Source text after filters: ")
	#print(source+"\n")
	return source

def printMenu():
	print "\n	COMMANDS		DESCRIPTION\n"
	print "	menu 			Show program menu\n"
	print "	generate 		Generate dictionary from source folder\n"
	print "	load  			Load generated dictionary\n"
	print "	perp  			Get perplexity\n"
	print "	prob [string]		Gets probability of the given text\n"
	print "	count [string]		Gets the nGram count of the given text\n"
	print "	set size [integer]	Sets the max n-gram size for n-gram"
	print "				creation and retreival\n"
	print "	exit 			Close program\n"
	
printMenu()	
print
userIn = raw_input("Enter command: ")
while userIn != 'exit':
	if userIn == "menu":
		printMenu()
	elif userIn == "generate":
		generateDictionary()
	elif userIn == "load":
		loadDictionary()
	elif userIn == "perp":
		print getPerp()
	elif userIn.startswith("prob"):
		if(dictionary != {}):
			print getProb(userIn[5:], maxNGramSize)
		else:
			print "Dictionary is not loaded. Run \"load\""
	elif userIn.startswith("count"):
		if(dictionary != {}):
			print getCount(userIn[6:])
		else:
			print "Dictionary is not loaded. Run \"load\""
	elif userIn.startswith("set size"):
		newSize = int(userIn[8:])
		if(newSize > 0):
			maxNGramSize = int(userIn[8:])
			print ("maxNGramSize = " + str(maxNGramSize))
		else:
			print "Integer must be > 0"
	else:
		print "Invalid command"
	print
	userIn = raw_input("Enter command: ")
import re

if __name__ == "__main__":
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
	'''
	wordRegex = re.compile(regex, re.VERBOSE)
	
	m = re.finditer(wordRegex, " dghe Greek --prefix tele-- ?(meaning \"distant\") to the Latin verb portare (meaning \"to carry\"). Fort's first use o the word was in the second a'via'ds of his 1931 book, Lo!: \"Mostly in this book I shall specialize upon indications that there exists a transportory force that I shall call Teleportation.\" Fort added \"I shall be accused of having assembled lies, yarns, hoaxes, and superstitions. To some degree I think so myself. To some degree, I do not. I offer the data.\") ")
	
	for n in m:
		print "%02d:%02d : \"%s\"" % (n.start(1), n.end(1), n.group(1))
	'''
	
	emoticons = """ 
	:-) :) :o) :] :3 :c) :> =] 8) =) :} 
	:^) :?) :-D :D 8-D 8D x-D xD X-D XD 
	=-D =D =-3 =3 B^D :-)) >:[ :-( 
	:( :-c :c :-< :?C :< :-[ :[ :{ ;( :-|| 
	:@ >:( :'-( :'( :'-) :') D:< 
	>:O :-O :O 8-0 :* :^* 
	;-) ;) ;-] ;] ;D ;^) :-, >:P :-P 
	:P X-P x-p xp XP :-p :p =p :-b :b 
	>:\ >:/ :-/ :-. :/ :\ =/ 
	=\ :L =L :S >.< :| :-| :$ :-X :X :-# :# 
	O:-) 0:-3 0:3 0:-) 0:) 0;^) >:) 
	>;) >:-) }:-) }:) 3:-) 3:) o/\o ^5 >_>^ ^<_< 
	|;-) |-O :-& :& #-) %-) %) 
	:-###.. :###.. <:-| ?_? <*)))-{ ><(((*> ><> 
	\o/ *\0/* @}-;-'--- @>-->-- 
	~(_8^(I) 5:-) ~:-\ //0-0\\ *<|:-) =:o] ,:-) 7:^] <3 </3
	D; D= DX v.v D-': D: D8 """
	
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
		[\.,LS$@\(\)\[\]\{\}xX0OoD3Dc\<\>\/\\\|pP]+				# mouth
						# bottom
						
					# right-to-left faces
				# vertical
				
			# symbols ???
		)
	)
	\S*?
	(?:\s)
	"""
	emoticonsRegex = re.compile(emoticonsRegex, re.VERBOSE);
	
	hashtags = "some stuff #hash-tag good"
	hashtagRegex = r"""
	(?=
		(?:
			\s
			\#
			\w+
			\s
		)
	)
	(?:\s+)												# consume at least one space
	\#
	(?:[^-'a-zA-Z]*)									# consume all other non base-word characters
	"""
	
	'''
	hashtagRegex = re.compile(hashtagRegex, re.VERBOSE)	
	print re.sub(hashtagRegex, "[match]", hashtags)
	
	'''
	print "------", sum(1 for _ in re.finditer(regex, emoticons)), "EMOTICONS MATCHED ------"
	print re.sub(regex, "[LN]", emoticons)
	'''
class NGram:
	items = []
	count = 0
	counter = 0
	
	def __init__(self, size):
		self.count = size
		self.items = [None] * size
		
	def addWord(self, word):
		if self.count > 0:
			self.items[len(self.items)-self.count] = word
			self.count -= 1
			self.counter += 1
			
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.items == other.items
		else:
			return false
			
	def __str__(self):
		if self.counter > 0:
			return str(len(self.items)) + '-GRAM\t' + ' '.join(self.items)
		else: 
			return ""

	def __hash__(self):
		if self.count == 0:
			return hash(' '.join(self.items))
		else:
			return hash("");
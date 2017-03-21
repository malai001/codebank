class li:
	def __init__(self):
		self.value = [1,2,3]
		
	def length(self):
		if self.value == None:
			return(0)
		else:

			return(len(self.value))
a = li()
print a.length()
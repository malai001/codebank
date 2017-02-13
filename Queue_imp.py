class Queue:
	
	def __init__(self):
		self.stack=[]
		self.size = 0 
		self.top  = -1

	def push(self,d):
		self.stack.append(d)
		self.size += 1
		self.top  += 1 
	
	def pop(self):
		if not (self.size == 0):
			p = self.stack[self.top]
			self.size -= 1
			self.top  -= 1
			return p
		else:
			print("Sorry Underflow")
	
	def enqueue(self,d):
		self.push(d)
	
	def dequeue(self):
		stack2=[]
		temp_size = self.size
		for i in xrange(temp_size,1,-1):
			stack2.append(self.pop())
		print("Dequeued element is",self.pop())
		self.stack=[]
		for i in range(len(stack2)):
			self.push(stack2[i])
	
	def print_queue(self):
		for i in range(self.size):
			print self.stack[i]



q=Queue()
q.enqueue(2)
q.enqueue(3)
q.print_queue()
q.dequeue()
q.dequeue()


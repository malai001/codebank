# Enter your code here. Read input from STDIN. Print output to STDOUT
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
		s = ''
		stack2=[]
		temp_size = self.size
		for i in xrange(temp_size,1,-1):
			stack2.append(self.pop())
		self.pop()
		self.stack=[]
		for i in range(len(stack2)):
			self.push(stack2[i])
		if(self.size>=0):
			s = self.stack[self.top]
		return s


q=Queue()
for i in range(0,input()):
	a = []
	s = ''
	a = map(int,raw_input().split(' '))
	if(a[0] == 1):
		q.enqueue(a[1])
	elif(a[0] == 2):
		s = q.dequeue()
	elif(a[0] == 3):
		s = q.dequeue()
		print s
    
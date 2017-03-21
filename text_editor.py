class stac:
	def __init__(self):
		self.stack = []
		self.redo =  []
		self.size = 0
		self.top = -1
	def push(self,key):
		self.stack.append(key)
		self.size +=1
		self.top  +=1
	def pop_print(self):
		p = ''
		if not (self.size == 0):	
			p = self.stack[self.top]
			self.top -=1
		return p
	def pop(self):
		if not (self.size == 0):	
			l = self.stack[self.top]
			del self.stack[-1]
			self.size -=1
			self.top  -=1
		return l		
s = stac()
for i in range(input()):
	a = raw_input().split(' ')
	if(int(a[0]) == 1):
		c = map(str,a[1])
		val = a[1]+'1'
		s.redo.append(val)
		for i in c:
			s.push(i)
	elif(int(a[0]) == 2):
		c = int(a[1])
		val1 = ''
		if(c<=s.size):
			for i in range(0,c):
				k = s.pop()			
				val1+=k
			val1 +='2'
			s.redo.append(val1)
	elif(int(a[0]) == 3):
		c = int(a[1])-1
		if(c<=s.size):
			l = s.top
			for i in range(0,s.size-c):
				k1 =s.pop_print()	
			print k1
			s.top = l
	
	elif(int(a[0]) == 4):
		i1 = s.redo[len(s.redo)-1]
		k = map(str,i1)
		if (k[len(k)-1] == '1'):
			for i in range(0,len(k)-1):
				s.pop()
			del s.redo[-1]
		if (k[len(k)-1] == '2'):
			for i in range(len(k)-2,-1,-1):
				s.push(k[i])
			del s.redo[-1]	
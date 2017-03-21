class stack:
	def __init__(self):
		self.stack = []
		self.size = 0
		self.top = -1

	def push(self,d):
		
		self.stack.append(d)
		self.size +=1
		self.top +=1
	
	def pop(self):
		
		if not(self.size >= 0):
			t=  self.stack[self.top]
			del self.stack[-1]
			self.size -= 1
			self.top  -= 1
			return t
		else:
			self.size = -1
			#print("stack underflow")

t= input()
for i in range(0,t):
	a =[]
	flag = 0 
	v = raw_input()
	for i in v:
		a.append(i)
	s = stack()
	for i in range(0,len(a)):
#[](){()
		if( a[i] == '{' or a[i] == '(' or a[i] == '['):
			s.push(a[i])
		elif(a[i] == '}' or a[i] == ')' or a[i] == ']'):
			if(s.size>0):
				s.pop()
			else:
				flag = 1
			# if(a[i] == '}' and t !='{'):
			# 	print ('NO')
# 			6
# }][}}(}][))]
# [](){()}
# ()
# ({}([][]))[]()
# {)[](}]}]}))}(())(
# ([[)
# NO
# YES
# YES
# YES
# NO
# NO
			# 	flag = 1
			# 	break
			# elif(a[i] == ')' and t !='('):
			# 	print ('NO')
			# 	flag = 1
			# 	break
			# elif(a[i] == ']' and t !='['):
			# 	print ('NO')
			# 	flag = 1
			#	break	
	#print s.stack	
	if (s.size == 0 and flag !=1):
	 	print ("YES")
	elif(s.size !=0 ):
		print ("NO")
	elif(flag == 1):
		print ("NO")
			
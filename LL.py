class stack:
	def __init__(self):
		self.stack = []
		self.top = -1
		self.size = 0
	
	def push(self,key):
		self.stack.append(key)	
		self.size+=1
		self.top = self.stack[-1]

	def pop(self):
		if self.size >=0:
			k = self.stack[-1]
			del[self.stack[-1]]
			self.size -=1 
		else:
			self.size -=1
		return k

class Node:
	def __init__(self,key):
		self.next =None
		self.val=  key

def push_node(root,s):
	if root:
		s.push(root.val)
		push_node(root.next,s)

def comp_node(root,s):
	flag = 0
	while(root !=None):
		if root.val == s.pop():
			#print root.val
			root = root.next
			flag = 1
		else:
			print 'Not Match'
			break
	return flag		

root = Node('R')
root.next = Node('A')
root.next.next = Node('D')
root.next.next.next = Node('A')
root.next.next.next.next = Node('R')
s = stack()
push_node(root,s)
if comp_node(root,s) == 1:
	print 'LL is a palindrome'
else:
	print 'LL is not a palindrome'
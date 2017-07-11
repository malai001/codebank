class tree:
	def __init__(self,key):
		self.val = key
		self.left = None
		self.right = None

def left_node_count(root,count):
	temp = root
	
	#while temp != None:
	count+=1
	print temp.val
	if temp.left:	
		count = left_node_count(temp.left,count)
	
	return count,'val'

def right_node_count(root,count):
	temp = root
	count+=1
	print temp.val
	if temp.right:
		right_node_count(temp.right,count)
	return count,'val'

			
def getleafcount(root):
	if root is None:
		return 0
	elif (root.left == None and root.right == None):
		return 1
	else:
		return getleafcount(root.left)+getleafcount(root.right)

def max_depth(root):
	if root is None:
		return 0
	else:
		ld = max_depth(root.left)
		#print ld,'lft',root.val
		
		rd = max_depth(root.right)
		#print rd,'rght',root.val
		if(ld>rd):
		 	return ld+1
		else:
		 	return rd+1	

def print_given_level(root,lvl,l):
	#print lvl

	if root == None:
		return 
	
	if l[0] < lvl:
		print root.val
		l[0]= lvl
	# elif l[0]<lvl :
	# 	#l.append(root.val)
	# 	print root.val,l
	# 	l[0] = lvl
		
		
	# 	#if not(flg): 
	print_given_level(root.left,lvl+1,l)
	print_given_level(root.right,lvl+1,l)
		# else:
		# 	print_given_level(root.left,lvl-1,flg)
		# 	print_given_level(root.right,lvl-1,flg)

def print_level(root):
	l = [0]
	print_given_level(root,1,l)
	

# root = tree(12)
# root.left = tree(5)
# root.left.left = tree(3)
# root.left.left.left = tree(1)
# root.left.left.right = tree(9)
# root.left.left.right.left = tree(2)
# root.left.left.right.right = tree(6)
# root.left.left.right.right.left = tree(4)
root = tree(12)
root.left = tree(10)
root.right = tree(30)
#root.left.left = tree(5)
#root.left.right = tree(6)
root.right.left = tree(25)
root.right.right = tree(40)
# print left_node_count(root,0)
# print right_node_count(root,0)
#print getleafcount(root)
#print max_depth(root)
print_level(root)
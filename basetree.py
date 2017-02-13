class Node:
	def __init__(self,key):
		self.val=key
		self.left=None
		self.right=None
	
def printNode(root):
	if root:
	 	print(root.val)
		printNode(root.left)
		printNode(root.right)
	
def print_level_order(root,k,ltr):
#	for i in range(0,k+1):
	for i in range(0,k+1):
		Printgiven(root,i,ltr)		
		ltr = ~ltr
		#print(ltr)

def Printgiven(root,level,ltr):
	if root is None:
		return 0
	if(level==1):
		print (root.val)
	elif(level>1):
		if not(ltr):
			Printgiven(root.left,level-1,ltr)
			Printgiven(root.right,level-1,ltr)
		else:
			Printgiven(root.right,level-1,ltr)
			Printgiven(root.left,level-1,ltr)
			
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
		rd = max_depth(root.right)

		if(ld>rd):
			return ld+1
		else:
			return rd+1	

def isSum(root):
	left_data =0
	right_data =0
	if (root is None or (root.left == None and root.right == None)):
			return 1
	else:
		if(root.left!= None):
			left_data = root.left.val
			print left_data
		if(root.right!= None):
			right_data = root.right.val
			print right_data
		if(root.val == left_data+right_data and isSum(root.left) and isSum(root.right)):
			return 1
		else:
			return 0

def isTarget(root,Key1):
	if(root == None):
		return 0
	if(root.val == Key1):
		return 1
	if(isTarget(root.left,Key1) or isTarget(root.right,Key1)):
		print(root.val)
		return 1
	return 0	

def isBinaryTree(root1,root2):
	if(root1 == None and root2 == None):
		return True
	if(root1 == None or root2 == None):
		return false
	return (root1.val == root2.val and isBinaryTree(root1.left,root2.left) and isBinaryTree(root1.right,root2.right))

def isIdentical(root1,root2):
	if(root2 == None):
		return True
	if(root1 == None):
		return false
	if(isBinaryTree(root1,root2)):
		return True
	return isIdentical(root1.left,root2) or isIdentical(root1.right,root2)	

def diameter(root):
	if root:
		ldp = max_depth(root.left)
		rdp = max_depth(root.right)
		ldm = diameter(root.left)
		rdm = diameter(root.right)
		return max(ldp+rdp+1,max(ldm,rdm))

def top_View_tree_left(root):
	if root:
		top_View_tree_left(root.left)
		print(root.val),	
def top_View_tree_right(root):
	if root:
		print (root.val),
		top_View_tree_right(root.right)

root=Node(3)
root.left=Node(5)
root.right=Node(2)
root.left.left=Node(1)
root.left.right=Node(4)
root.right.left=Node(6)
root.right.right = Node(7)
root.left.left.right= Node(9)
root.right.right.left = Node(8)

# root1 = Node(5)
# root1.left = Node(3)
# root1.left.left = Node(8)

#n = raw_input()
#print(isTarget(root1,8))
#print(isIdentical(root,root1))
#root.right.right=Node(7)
#root.right.right.left=Node(8)
#printNode(root)		
#h=max_depth(root)
#print (getleafcount(root))
#print(isSum(root))
#print(h)
print_level_order(root,max_depth(root),0)
# print(diameter(root))
# print(diameter(root))
# top_View_tree_left(root)
# top_View_tree_right(root.right)


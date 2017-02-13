# class Node:
# 	def __init__(self,key):
# 		self.value=key
# 		self.left=None
# 		self.right=None
# # def var():
# # 	global count
# # 	count=0	
# def print_node(temp,count):
# 	if temp:
# 		print(temp.value)
# 		print_node(temp.left,count)
# 		count = print_node(temp.right,count)		
# 	return count+1
# root = Node(1)
# root.left=Node(2)
# root.right=Node(3)
# root.left.left=Node(4)
# root.left.right=Node(5)
# global count 
# count = print_node(root,1)
# print(count)
class Node:
 
    # Constructor to create a new node
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
 
# Compute the "maxDepth" of a tree -- the number of nodes 
# along the longest path from the root node down to the 
# farthest leaf node
def maxDepth(node):
    if node is None:
        return 0 ; 
 
    else :
 
        # Compute the depth of each subtree
        lDepth = maxDepth(node.left)
    	rDepth = maxDepth(node.right)
	print(lDepth)
	print(rDepth)
    # Use the larger one
        if (lDepth > rDepth):
    		#print(lDepth)
         	return lDepth+1
        else:
        	#print(rDepth)
            return rDepth+1
 
 
# Driver program to test above function
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
 
 
print "Height of tree is %d" %(maxDepth(root))

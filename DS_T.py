class Node:
	def __init__(self,key):
		self.left=None
		self.right=None
		self.val=key

def print_node(temp):
		if temp:
			print_node(temp.left)
			print_node(temp.right)	
			print(temp.val)
def print_BFS(temp):
	
	print(temp.height)

root = Node(1)
root.left=Node(2)
root.right=Node(3)
root.left.left=Node(4)
root.left.right=Node(5)

print_node(root)
print_BFS(root)
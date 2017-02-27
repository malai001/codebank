class Node:
	def __init__(self,val):
		self.key = val
		self.left = None
		self.right = None
	
def mirror_root(root):
	if root == None:
		return None
	if root:
		Left = Node(None)
		Right = Node(None)
		Left = mirror_root(root.left)
		Right = mirror_root(root.right)
		root.left = Right
		root.right = Left
	return root

def inorder(root):
	if root:
		inorder(root.left)
		print root.key,
		inorder(root.right)

root =  Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
inorder(root)
root = mirror_root(root)
inorder(root)

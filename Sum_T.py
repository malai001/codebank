class trie:
	def __init__(self,key):
		self.left=None
		self.right=None
		self.value=key
def PrintTrie(Node):
	if Node:	
		PrintTrie(Node.left)
		print(Node.value)
		PrintTrie(Node.right)

root=trie(1)
root.left=trie(2)
root.right=trie(3)
root.left.left = trie(4)
root.left.right = trie(5)

PrintTrie(root)

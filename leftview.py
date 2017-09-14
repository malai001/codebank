class tree:
	def __init__(self,key):
		self.val = key
		self.left = None
		self.right = None

def print_tree(root):
	if root != None:
		print(root.val)
		print_tree(root.left)
#		print_tree(root.right)

def left_v(root,level,m_l):
	if root is None:
		return
	print m_l, level
	if level > m_l[0]:
		print root.val
		m_l[0] = level
	left_v(root.left,level+1,m_l)
	left_v(root.right,level+1,m_l)

def left_view(root):
	m_l = [0]
	left_v(root,1, m_l)

root = tree(2)
root.left = tree(3) 
root.right = tree(4)
root.left.left = tree(5)
root.left.right = tree(6)
root.right.left = tree(7)
root.right.right = tree(8)

left_view(root)
#print_tree(root)
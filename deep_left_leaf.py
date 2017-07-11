class tree:
	def __init__(self,val):
		self.key = val
		self.left = None
		self.right = None

def deepest_left(root,lvl,maxlvl,isleft):
	if root is None:
		return
	if isleft:
		if root.left is None and root.right is None:
			if lvl >maxlvl[0]:
				deepest_left.res = root
				maxlvl[0] = lvl
				#print maxlvl[0],deepest_left.res.key
				return
	deepest_left(root.left,lvl+1,maxlvl,True)
	deepest_left(root.right,lvl+1,maxlvl,False)

def deep_left(root):
	maxlvl = [0]
	deepest_left.res = None
	deepest_left(root,0,maxlvl,False)
	return deepest_left.res.key
# def print_rec(root,lvl):
# 	if root is None:
# 		return 0 
# 	if lvl == 1:
# 		print root.key		
# 	else:
# 		print_rec(root.left,lvl-1)
# 		print_rec(root.right,lvl-1)

# def print_gvn(root):
# 	h = height(root)
# 	print_rec(root,h)

root = tree(3)
root.left = tree(2)
root.right = tree(5)
root.left.left = tree(1)
root.left.right = tree(4)

print deep_left(root)
# print_gvn(root)

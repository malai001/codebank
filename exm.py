class exm:
	def __init__(self,key):
		self.value=key
		self.left=None
		self.right=None

a = exm(3)
a.left = exm(4)
a.right = exm(5)

print(a.value)
print(a.left.value)
print(a.right.value)

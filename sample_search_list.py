import re
a = []
pattern = '''_abc'''
msg = ['05_abc','06_ced']
for i in msg:
	c = i.split('_')
	a.append(c[0])

print (max(a))

s = max(a)+'_ced'
print s




a = [[0,1,0],[1,0,1],[0,1,0]]
s = ''
for i in a:
	for j in i:
		s += str(j)
	s+=","	
b = s.split(',')
a =[]
for i in range(0,len(b)):
	if b[i] not in a and  b[i] !='':
		a.append(b[i])
print a		
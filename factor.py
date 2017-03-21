l =[]
for i in range(1,a):
	if(a%i == 0):
		l.append(i)
if (sum(l) == a):
	print('True')
else:
	print('False')
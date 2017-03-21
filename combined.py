a = ['abcd1','xyz2']
for i in a:
	k = map(str,i)
	if (k[len(k)-1] == '1'):
		print k
	if (k[len(k)-1] == '2'):
		print k	
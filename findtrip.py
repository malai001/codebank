a = [8,5,1,2,3,4,6]
l = 0
h = 1
k = 14
for i in range(0,len(a)):
	for j in range(0,len(a)):
		if(j == l or h == j):
			j +=1
		else:
			if(a[l]+a[h]+a[j] == k):
				print 'found',
				print a[l],a[h],a[j]
	l += 1
	h =l+1
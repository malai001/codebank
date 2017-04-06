f,n = map(int,raw_input().split(' '))
a = map(int,raw_input().split(' '))
for m in range(0,f):
	i = map(int,raw_input().split(' '))
	k = i[0]
	l = i[1]
	min1 = 9999
	for g in range(k,l+1):
		if(a[g]<min1):
			min1 = a[g]
	print min1


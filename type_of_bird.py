n =input()
a = map(int,raw_input().split(' '))
k = n
for i in range(0,len(a)):
	a[a[i]%k]+=k
max1 = a[0]
r = 0	
for i in xrange(1,len(a)):
	if(max1<a[i]):
		max1 = a[i]
		r = i
print r

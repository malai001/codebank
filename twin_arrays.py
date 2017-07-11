n = input()
a = map(int,raw_input().split(' '))
b = map(int,raw_input().split(' '))
res = 9999
for i in xrange(n):
	for j in xrange(n):
		if i!=j and res >a[i]+b[j]:
	#		if res>a[i]+b[j]:
			res = a[i]+b[j]
print res
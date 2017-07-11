n = input()
a = map(int,raw_input().split(' '))
m = 9999
a = sorted(a)
for i in xrange(0,n):
	j = i+1
	
	if j>n-1:
		j = j%n
	if a[i]<0:
		a[i]=-a[i]
	if a[i]>a[j]:
		if m>a[i]-a[j]:
			m = a[i]-a[j]
	elif a[j]>a[i]:
		if m >a[j]-a[i]:
			m = a[j]-a[i]		
print m			
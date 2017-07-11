n = input()
a = map(int,raw_input().split(' '))
v = a[0]
mi = 9999
for i in range(1,n):
	for k in range(i,n):
		if(v == a[k]):
			if (mi >k-a.index(v)):
				mi = k-a.index(v)
			break	
	v = a[i]		
if mi == 9999 :
	print -1
else:
	print mi
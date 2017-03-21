N,k = map(int,raw_input().split(' '))
a = []
for i in range(1,N+1):
	a.append(i)
#print a
count = 0
for i in range(0,len(a)-1):
	for j in range(i+1,len(a)):		
		prod = a[i]&a[j]
		if (prod<k and prod !=0):
			if (count < prod):
				count = prod
print count		

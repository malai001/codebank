n = input()
a = map(int,raw_input().split(' '))
v = map(int,raw_input().split(' '))

count = 0
s = 0
if(n>1):
	for i in range(0,n-1):
		for j in range(i,i+v[1]):
			if (j == n):
				break	
			s += a[j]
			
		if(s == v[0]):
			print s	
			count +=1	
		s = 0	
			
elif(n==1 and v[1] == 1):
	if (v[0] == a[0]):
		count += 1		
print count	
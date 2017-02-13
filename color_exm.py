n = int(raw_input().strip())
A = map(int,raw_input().strip().split(' '))
min=0
for i in range(0,n-1):
	for j in range(i+1,n-1):
		if(A[i]==A[j]):
			print (A[j])
			min=abs(i-j)

if(min==0):
	min= -1
print (min)	

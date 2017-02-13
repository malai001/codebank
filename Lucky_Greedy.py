N,K =map(int,raw_input().split(' '))
important = []
total =0
for i in range(0,N):
	l,imp = map(int,raw_input().split(' '))
	total =total + l
	if(imp == 1):
		important.append(l)
important.sort()
n=len(important)-K
for i in range(0,n):
	total =  total-2*important[i]
print total
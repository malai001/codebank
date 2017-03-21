import sys
a = raw_input().split()
b = raw_input().split()
co  = 0
c = 0
for i in range(0,len(a)):
	if(a[i]>b[i]):
	 	co +=1
	if(a[i]<b[i]):
		c += 1
print co,
print c
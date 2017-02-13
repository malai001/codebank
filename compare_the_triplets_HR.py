import sys

a = raw_input().split()
b = raw_input().split()
count  = 0
count1 = 0
for i in range(0,len(a)):
	if(b[i]>a[i]):
		count1 +=1
	elif(a[i]>b[i]):
		count += 1
print count,
print count1

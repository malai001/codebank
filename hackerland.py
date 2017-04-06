
n = map(int,raw_input().split(' '))
a = map(int,raw_input().split(' '))


a = sorted(a)
l =0
k =0
flag = 0
count = 0
m = 2*n[1]
while(l<len(a)):
	j = a[l]+m
	
	if(j<=a[len(a)-1]):
		for i in range(0,j):
			if(a[k] <=j):
				a[k] = -1
				flag = 1
				k+=1
		l = k
		if(flag == 1):
			count +=1
			flag = 0
	else:
		break
if(j>a[len(a)-1]):
		count +=1
			
print count
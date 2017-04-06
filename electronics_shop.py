k = map(int,raw_input().split(' '))
a = map(int,raw_input().split(' '))
b = map(int,raw_input().split(' '))

upd= 0
flag = 0
for i in range(0,k[1]):
	for j in range(0,k[2]):
		if(a[i]+b[j] == k[0]):
			print k
			flag = 1
			break
		elif(a[i]+b[j] <k[0]):
			if(a[i]+b[j]>upd):
				upd = a[i]+b[j]
				flag = 1
else:
	if(flag != 1):
		print -1
	else:
		print upd	
v = map(int,raw_input().split(' '))
a = map(int,raw_input().split(' '))
count = 0

for j in range(0,v[0]):
	if a[j]>=v[1]:
		if a[j]%v[1] == 0 and a[j] != v[1]:
			a[j] = a[j]/v[1]
		else:
			a[j] = a[j]%v[1]
		 

	elif(a[j]<v[1] and a[j]>0):
		a[j] = a[j]-v[1]
a = sorted(a)
val = 0
for i in a:
	if i<=0:
		count+=1
	elif(i>0):
		count+=1
	if count == v[2]:
		break
	val +=1			
print val
n = input()
a = map(int,rawinput().split(' '))
min1 = a[0]
max1 = a[0]
min_c = 0
max_c = 0 
for i in range(1,n):
	if(a[i]>max1):
		max1 = a[i]
		max_c +=1
	if(a[i]<min1):
		min1 = a[i]
		min_c +=1
print max_c,
print min_c

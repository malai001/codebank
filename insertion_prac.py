a = [2,1,3,1,2]
count =0
for i in range(1,len(a)):
	key = a[i]
	j = i-1
	while(j>=0 and a[j]>key):
		a[j+1] = a[j]
		j-=1
		count += 1
	a[j+1] = key
print a
print count
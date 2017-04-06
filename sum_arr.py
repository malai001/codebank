a = [5,4,2,1,2]
a.sort()
mid = 1
while(mid != len(a)):

	print sum(a[mid+1:])

	mid +=1

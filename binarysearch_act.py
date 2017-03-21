a = [1,2,3,4,5,5,7]
l = 0
h= len(a)
x = 5
while(l<=h):
	mid = l+(h-l)/2
	if(a[mid] == x):
		print 'found at pos',mid
		break
	elif(a[mid]<x):
		l = mid + 1
	else:
		h = mid - 1


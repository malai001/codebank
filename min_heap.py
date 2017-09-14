a = [100,97,93,38,67,54,93,17,25,42]
n = len(a)

def heapify(a,n,i):
	lr = i
	l = 2*i+1
	r = 2*i+2
	print i,l,r
	if (l<n and a[i]>a[l]):
		lr = l
		print lr,'**',a[i],a[l]
	if(r<n and a[lr]>a[r]):
		lr = r
		print lr,'++',a[i],a[r]
	if lr!=i:
		a[i],a[lr] = a[lr],a[i]
		print a
		heapify(a,n,lr) 


for i in xrange(n,-1,-1):

	heapify(a,n,i)
	print a
print a
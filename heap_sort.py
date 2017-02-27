a = [5,4,2,7,6,1,3,2,7,7,7]
def heapify(a,n,i):
	lar =i
	l = 2*i+1
	r = 2*i+2
	if(l<n and a[i]<a[l]):
		lar = l
	if(r<n and a[lar]<a[r]):
		lar = r
	if(lar != i ):
		a[i],a[lar] = a[lar],a[i] 
		heapify(a,n,lar)
def heap_sort(a):	

	n = len(a)
	for i in range(n, -1, -1):
		heapify(a, n, i)
	for i in range(n-1, 0, -1):
		a[i], a[0] = a[0], a[i] 
 	  	heapify(a, i, 0)		

heap_sort(a)
print a
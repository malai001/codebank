a = [5,4,2,7,6,1,3,2,7,7,7]
def merge_arr(a,l,m,r):
	n1 = m-l+1
	n2 = r-m
	L = [0]*(n1)
	r = [0]*(n2)
	for i in range(0,n1):
		L[i] = a[l+i]
	
	for j in range(0,n2):
		r[j] = a[m+1+j]
	i=0
	j=0
	k=l
	while(i<n1 and j<n2):
		if(L[i] <= r[j]):
			a[k] = L[i]
			i+=1
		else:
			a[k]=r[j]
			j+=1
		k+=1
	
	while (i<n1):
		a[k] = L[i]
		i+=1
		k+=1
	while(j<n2):
		a[k] = r[j]
		j+=1
		k+=1
	
def merge_sort(a,l,r):
	if(l<r):	
		m = (l+(r-1))/2
		merge_sort(a,l,m)
		merge_sort(a,m+1,r)
		merge_arr(a,l,m,r)
	return a	
a = merge_sort(a,0,len(a)-1)
print a
# for i in range(10,-1,-1):
# 	print i
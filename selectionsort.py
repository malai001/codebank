a = [5,4,2,7,6,1,3,2,7,7,7]

def selection_sort(A):
	for i in range(0,len(a)):
		min_i = i
		for j in range(i+1,len(a)):
			if(a[j]<a[min_i]):
				min_i = j
		temp = a[min_i]
		a[min_i] = a[i]
		a[i] = temp
	return a

def remo(a):
	d={}
	l=0
	for k in range(0,len(a)):
		d[a[k]] = a.count(a[k])
		l+=1
	l =0 
	a = [None]*len(d.keys())
	for k in d.keys():
		if(d[k] >=1):
			a[l] = k
			l+=1
			d[k] = -1
	print a

a = selection_sort(a)
remo(a)

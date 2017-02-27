a = [5,4,2,7,6,1,3,2,7,7,7]
def sort (a):
	for i in range(0,len(a)):
		for j in range(0,len(a)):
			if(a[i]<a[j]):
				temp = a[i]
				a[i] = a[j]
				a[j] = temp
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
a = sort(a)
remo(a)
a = [5,4,2,7,6,1,3,2,7,7,7]
def  insertion_sort(a):
	for i in range(0,len(a)):
		key = a[i]
		j =i-1
		while(j>=0 and a[j]>key):
			a[j+1] = a[j]
			j -=1
			print a
		a[j+1] = key
		print a
	return a
# def remo(a):
# 	d={}
# 	l=0
# 	for k in range(0,len(a)):
# 		d[a[k]] = a.count(a[k])
# 		l+=1
# 	l =0 
# 	a = [None]*len(d.keys())
# 	for k in d.keys():
# 		if(d[k] >=1):
# 			a[l] = k
# 			l+=1
# 			d[k] = -1
# 	print a
a = insertion_sort(a)
remo(a)
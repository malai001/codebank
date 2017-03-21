a = [1,2,3,1,2,3]
l = 0
m = 0
h = len(a)-1
while(m<=h):
	if(a[m]==1):
		a[l],a[m] = a[m],a[l]
		l+=1
		m+=1
	elif(a[m]==2):
		m+=1
	else:
		a[h],a[m] = a[m],a[h]
		h-=1

print a		
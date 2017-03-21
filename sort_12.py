a= [0,1,1,0,1,1,0,0]
l = 0
h = len(a)-1
for i in range(0,len(a)/2):
	if(a[l]>a[h]):
		a[l],a[h] = a[h],a[l]
		l+=1
		h-=1
	elif(a[l]==0):
		l+=1
	elif(a[h]==1):
		h-=1
	else:
		l+=1
		h-=1
print a
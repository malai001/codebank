n= int(raw_input())
sumin = n
d = []
i=1
l=1
while(i<=n):
	if(n==1):
		print n
		print n
		break
	if(sumin>0):
		sumin = sumin -i
		d.append(i)
		l=sum(d)
#		print l
		if(l>n):
			del d[-1]
			k=abs(sum(d)-n)
			d[-1] = d[-1]+k
		 	print len(d)
		 	print " ".join([str(i) for i in d])
		 	break
		#elif(l==1 and l<n):
			#print len(d)
 	elif(sumin <= 0):
		print len(d)
		print " ".join([str(i) for i in d])
		break 
	i=i+1

count = 1
n,m = map(int,raw_input().split())
if(n>=m):
	for i in range(1,m+1):
		print i 
elif(m>n):
	count1 = 2*n+1
	temp = count1
	while(count1<=m and count<=(m/2)+1):
			print count1
			print count
			count1 = count1+1
			count  = count +1
	while(count<=(m/2)+1 and temp !=count):
		print count
		count +=1
else:
	if(m%2!=0):
		count1 =(m/2)+2
	else:
		count1 = (m/2)+1
	temp = count1
	#for i in range(1,m):
	while(count1<=m and count<=(m/2)+1):
			print count1
			print count
			count1 = count1+1
			count  = count +1
	while(count<=(m/2)+1 and temp !=count):
		print count
		count +=1

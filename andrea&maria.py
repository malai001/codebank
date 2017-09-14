a = [1,1]
b = [1,1]
val = 'Even'
ad = 0
flag = 0
mar = 0
if val == 'Even':
	i = 0
	for m in range(i,len(a),2):
		if(a[m] == b[m]):
			flag = 1
		c = a[m] - b[m]
		c1= b[m] - a[m]
		mar = mar+c1
		ad  = ad+ c
		
else:
	i =1
	for m in range(i,len(a),2):
		if(a[m] == b[m]):
			flag=1
		c = a[m] - b[m]
		c1= b[m] - a[m]
		mar += c1
		ad  += c

if(ad <mar):
	print 'Maria'
if(ad > mar and flag != 1):
	print 'Andrea'
elif(flag == 1):
	print 'Tie'	

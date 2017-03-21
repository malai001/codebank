
n = int(raw_input().strip())
p = int(raw_input().strip())
# your code goes here
c1= n-p
c1 = c1/2
c = 0
while(p>0):
	p=p-2
	if(p>=0):
		c+=1
if(c<c1):
	print c
else:
	print c1
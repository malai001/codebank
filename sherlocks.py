t = int(raw_input())
for x in range(0,t):
	a,b = map(int,raw_input().split(' '))
	count =0
	c=1 
	for i in range(a,b+1):
    	#mult = i*i
		c= pow(i,0.5)
		c = int(c)
		print c
		if((i % c) == 0):
			count = count + 1
	print count
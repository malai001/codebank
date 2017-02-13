n = 4
m = 3
k = 9
i = 0
b = 0
if (k % 2 != 0):
	side = 'L'
	while (k>i):
		i =i+(2*m)
		b = b+1
	y = b
	x = ((i-k)+1)/2
	print (x,y,side)
else:
	side = 'R'
	while (k>i):
		i =i+(2*m)
		print i
		b = b+1
	y = b
	x = (i - k )% m
	if (x ==0 ):
		x = x+m
	print (y,x,side)

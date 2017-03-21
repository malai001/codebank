def max3bad(x,y,z):
	maximum = 0
	print 
	if x>=y and x>=z:
		maximum = x
	elif y>=x and y>=z:
		maximum = y
	elif z>=x and z>=y:
		maximum = z
	return maximum

print max3bad(9,5,3)
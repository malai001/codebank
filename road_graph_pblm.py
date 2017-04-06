for i in range(input()):
	d = {}
	val = map(int,raw_input().split(' '))
	for y in range(0,val[1]):
		d[y]=map(int,raw_input().split(' '))
	if(val[2]<val[3]):
		print val[0]*val[2]
	else:
		print (val[1]-1)*val[3]+val[2]
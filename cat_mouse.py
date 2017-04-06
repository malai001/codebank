for i in range(input()):
	a = map(int,raw_input().split(' '))
	if(abs(a[2]-a[1])<abs(a[2]-a[0])):
		print ('Cat B')
	elif(abs(a[2]-a[1]) == abs(a[2]-a[0])):
		print ('Mouse C')
	elif(abs(a[2]-a[1])>abs(a[2]-a[0])):
		print ('Cat A')
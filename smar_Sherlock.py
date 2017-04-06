for i in range(input()):
	n = input()
	a = map(int,raw_input().split(' '))
	l = sum(a)-a[0]
	h = 0
	flag = 1
	if(n == 1):
		flag = 0
	else:        
		for i in range(1,len(a)):
			if(l == h):
				flag = 0
				break
			else:
				h += a[i-1]
				l -= a[i]
			print l,
			print h

	if(flag == 1):
		print 'NO'
	elif(flag == 0):
		print'YES'
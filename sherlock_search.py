for i in range(input()):
	n = input()
	a = map(int,raw_input().split(' '))
	sum1 = 0
	sum2 = 0
	l = sum(a[:mid])
	h = sum(a[mid+1:])
	mid = l+1
	flag = 1
	if(n == 1):
		print 'YES'
		flag = 0
	else:        
		while(mid!=len(a) and mid>0):	
			if(sum(a[:mid]) == sum(a[mid+1:])):
				print 'YES'
				flag = 0
				break
			l = sum(a[:mid])
			h = sum(a[mid+1:])
			mid+=1

	if(flag == 1):
		print 'NO'
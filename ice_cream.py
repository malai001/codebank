for t in range(input()):
	m = input()
	n = input()
	a = map(int,raw_input().split(' '))
	j = 0
	flag = 0
	for i in range(0,len(a)):
		f = m-a[i]
		for l in range(i+1,len(a)):
			if(f == a[l]):
				j = l	
				flag = 1
				break
		if(flag == 1):
			break
	if(i<j):	
		print i+1,
		print j+1
	else:
		print j+1,
		print i+1
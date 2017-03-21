for _ in range(input()):
	n,k = map(int,raw_input().split(' '))
	print (k-1 if (k-1|k) <= n else k-2)
for i in range(input()):	
	n= input()
	a = raw_input().split()
	flag = 0
	if(len(a) == 1 ):
		if(a[0]=='cookie'):
			flag =1
	if(a[len(a)-1]== 'cookie'):
		flag =1
	for i in range(0,len(a)-1):
		if (a[i] == 'cookie' and i+1<len(a)):
			if(a[i+1] != 'milk' ):
				flag = 1

	if (flag == 0):
		print 'YES'
	else:
		print 'NO'
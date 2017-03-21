t = input()
for i in range(0,t):
	sum_v=0
	fine=0
	flag = 0
	n = input()
	pattern = map(int,raw_input().split(' '))
	for i in pattern:
		if(i==0):
			fine +=100
			flag = 1 
			sum_v +=1000
		elif(i==1):
			sum_v +=0
			if(flag == 1):
				fine+=100
	print sum_v+fine
		


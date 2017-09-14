a = raw_input()
n  = input()
n1  = len(a)
flag = 0
ac = 0
if a !='a' and n1 !=1:
	for i in a:
		if i == 'a':
			ac +=1

	v = n/n1
	r = n%n1
	#print ac,v,r
	ac = ac*v
	for i in xrange(0,r):
		if a[i] == 'a':
			ac +=1
elif a=='a' and n1 == 1:
	flag = 1
	print n 
if flag !=1 :
	print ac
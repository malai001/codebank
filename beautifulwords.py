a = raw_input()
flag =0
b=['a','e','i','o','u']
for i in xrange(0,len(a)-1):
	j = i+1
	if (a[i]==a[j] or (a[i] in b and a[j] in b)):
		print 'no'
		flag = 1
		break
if flag !=1:
	print 'yes'		

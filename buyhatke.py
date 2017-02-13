
N =input()
count =0
a = map(int,raw_input().split(' '))
d ={ }
d = dict((x,a.count(x)) for x in set(a))
for i in a:
	if(d[i]>2):
		count = count+ d[1]-2
		d[i] = d[i] -2
print count	


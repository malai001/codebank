s = raw_input()
d = {'p': 0,'c':0,'m':0,'b':0,'z':0}
for i in s:
	d[i] +=1
c = d.values()
count = min(c)
for i in c:
	if(count>0):
		if i < count:
			count = count-1
if (count >=0):
	print count		
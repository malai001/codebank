n = input()
a = map(int,raw_input().split(' '))
d = {}
for i in a:
	if i not in d.keys():
		d[i] = 1
	else:
		d[i]+=1
print n-max(d.values())
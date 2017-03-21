a = map(int,raw_input().split(' '))
mn = -1
mx = 111111111
s = 0
for i in a:
	s+=i
	if(mn < i):
		mn = i
	if(mx > i): 
		mx = i
print sum(a)-mn,
print sum(a)-mx
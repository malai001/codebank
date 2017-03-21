#a = map(int,raw_input().split(' '))
a = [2,3,4,5,6]
s = 0
mx = -1
mn = 999999999
for i in a:
	s += i
for i in a :
	if(mx < s-i):
		mx = s-i
	if(mn > s-i):
		mn = s-i
print mn,
print mx
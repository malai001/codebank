n = input()
a = map(int,raw_input().split())
a = sorted(a,reverse = True)
s = 0
for i in range(0,n):
	s += (a[i]*pow(2,i))
print s
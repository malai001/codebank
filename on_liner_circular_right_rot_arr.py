v = map(int,raw_input().split(' '))
a = map(int,raw_input().split(' '))
n = v[0]
d = v[1]
q = v[2]
v =[]
for i in xrange(0,q):
	v.append(input())

for i in v:
	print a[(n-d+i)%n]

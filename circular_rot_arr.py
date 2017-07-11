v = map(int,raw_input().split(' '))
a = map(int,raw_input().split(' '))
n = v[0]
d = v[1]
q = v[2]
v =[]
for i in xrange(0,q):
	v.append(input())
def gcd(a,b):
	if b==0:
		return a
	else:
		return gcd(b,a%b)
k = gcd(n,d)
#k = d

for i in xrange(0,n-k):
 	a[i],a[n-k] = a[n-k],a[i]
print a	

for i in v:
	print a[i]
	
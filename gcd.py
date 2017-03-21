def gcd(a,b):
 	if a == 0:
 		return b
 	return gcd(b%a,a)
def left_rotate(a,d):
	n =len(a)
	for i in range(0,gcd(len(a),d)):
		j = i
		temp = a[i]
		while(1):
			k = j+d
			if(k>=n):
				k = k-n
			if(k==i):
				break
			a[j] = a[k]
			j = k
		a[j] =temp
	for i in a:
		print i,
n,d = map(int,raw_input().split())
a = map(int,raw_input().split(' '))
left_rotate(a,d) 
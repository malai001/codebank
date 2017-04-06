def fib(t1,t2,n):
	f = [0]*(n+1)
	if(n>1):
		f[0] = t1
		f[1] = t2
		for i in range(2,n+1):
			f[i] = 	f[i-2]+(f[i-1]*f[i-1])
	return f[n-1]
 
it = map(int,raw_input().split(' '))
print fib(it[0],it[1],it[2])

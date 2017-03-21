# Enter your code here. Read input from STDIN. Print output to STDOUT
n = input()
p = [0]*(n+1)
l = 0
k = map(int,raw_input().split(' '))
for i in range(1,n+1):
	p[k[l]] = i
	l+=1
for i in range(1,n+1):
	print p[p[i]]
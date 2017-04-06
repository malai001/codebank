n =input()
a = map(int,raw_input().split(' '))
c = [0]*(6)
for i in a:
	c[i] = c[i]+1
print c.index(max(c))
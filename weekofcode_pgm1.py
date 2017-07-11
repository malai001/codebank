n = input()
a=[]
for i in range(n):
	a.append(input())
k = max(a)
s = '0'
t=''
while(len(s)<=k):
	for j in s:
		if j == '0':
			t+='1'
		elif j == '1':
			t+='0'
	s = s+t
	t = ''

for i in a:
	print s[i]
a = map(int,raw_input().split(' '))
l = []
for k in range(a[2]): 
	l.append(map(int,raw_input().split(' ')))
#print l  
s = 0
for i in l:
	k = i[2]-i[1]
	s+=k+1
print(a[0]*a[1]-s) 
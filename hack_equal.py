n = input()
a = map(int,raw_input().split(' '))
count = 0
for i in range(0,n-1):
	if(a[i] != a[i+1]):
		count =count +1
print count-1


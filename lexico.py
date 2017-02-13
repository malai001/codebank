n =input()
a=[]
for i in range(0,n):
	a.append(input())
a.sort()
a.sort(key=len, reverse=False) 
print a
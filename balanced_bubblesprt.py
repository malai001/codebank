n = int(raw_input().strip())
a = map(int, raw_input().strip().split(' '))
count = 0
for i in range(0,len(a)-1):
    for j in range(1,len(a)):
        if(a[i]>a[j]):
        	a[j],a[i] = a[i],a[j]
           	count +=1
print 'Total Number of Swaps',count
print 'First Element',a[0]
print 'Last Element',a[len(a)-1]

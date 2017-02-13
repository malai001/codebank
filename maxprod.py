#code
t = input()
while(t>0):
    a=[]
    temp = []
    n = input()
    a = raw_input().split(' ')
    for i in range(0,n):
        a[i] =  int(a[i])
    a.sort()
    print (a[n-1]*a[n-2])
    t -= 1
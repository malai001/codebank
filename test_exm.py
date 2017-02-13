t = input()
while(t>0):
    n,k = map(int ,raw_input().split(' '))
    a = map(int,raw_input().split(' '))
    while(k>0):
        n =len(a)
        i=0   
        temp = a[i]*a[n-2]
        print a
        if(a[i+1]*a[n-1]<temp):
            del a[n-1] 
            if(len(a) == 2):
                break
        else:
            del a[0]
            if(len(a) == 2):
                break
        k = k-1 
    n = len(a)   
    print (a[0]*a[n-1])    
    t = t - 1
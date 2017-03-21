a=[1,0,2,0,1,2,1,0,0,1,1,1,1,0,0]
last=len(a)-1
first=0
n=last
for i in xrange(len(a)/2+1):
    if(a[i]==0 and i>first):
        a[i],a[first]=a[first],a[i]
    elif(a[i]==2 and i<last):
        a[i],a[last]=a[last],a[i]
    if(a[n-i]==0 and n-i>first):
        a[n-i],a[first]=a[first],a[n-i]
    elif(a[n-i]==2 and n-i<last):
        a[n-i],a[last]=a[last],a[n-i]
    while(a[first]==0):
        first+=1
    while(a[last]==2):
        last-=1
print a 
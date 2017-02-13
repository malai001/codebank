def pow(self,a,b):
   if(b):
     return multiply(a, pow(a, b-1))
   else:
    return 1    
 
/* A recursive function to get x*y */
def multiply(int x, int y):
   if(y):
     return (x + multiply(x, y-1))
   else:
     return 0
 
t = int(raw_input())
while(t):
    x,k,m = map(int,raw_input().strip().split(' '))
    #k = map(int,raw_input())
    #m = map(int,raw_input())
    #mult = x
    #while(k>0):
    #	mult = mult * x 
    #	k=k-1
    #print mult
    a =x
    while(k):
    	a = pow(a,x)
    	k=k-1
    print a % m 
    t=t-1
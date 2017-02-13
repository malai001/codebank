#/* Works only if a >= 0 and b >= 0  */
def pow(a,b):
  if (b == 0):
    return 1
  answer = a;
  increment = a;
  i = 1
  j = 1
  for i  in range(1,b):
     for j in range(1,a):
        answer =answer+increment;
     increment = answer;
  return answer
 
# /* driver program to test above function */
# int main()
# {
#   printf("\n %d", pow(5, 3));
#   getchar();
#   return 0;
# }

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
    a = x
    while(k):
    	a = pow(a,x)
    	k=k-1
    print a % m 
    t=t-1
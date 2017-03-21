d={}
i=0
c='y'
while(c!=''):
  c=input()
  d[i]=c
  i=i+1
for j in range(0,i):
  if((j+1)%3==0):
    print(d[j])
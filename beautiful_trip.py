n,d = map(int,raw_input().split())
c = map(int,raw_input().split(' '))

gc = 0
for i in range(len(c)):
    if c[i]+d in c and c[i]+2*d in c:
        gc+=1
print (gc)
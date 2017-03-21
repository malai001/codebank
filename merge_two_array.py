a = [1,5,6,9]
b = [2,4,7]
#[1,2,4,5,6,7]
n1 = len(a)+len(b)
c =[0]*(n1)
k =0
i = 0
j = 0 
while(i<len(a) and j<len(b)):
	if(a[i]<=b[j]):
		c[k] = a[i]
		i+=1
	else:
		c[k] = b[j]
		j+=1
	k+=1
while(i<len(a)):
	c[k] = a[i]
	i+=1
	k+=1

while(j<len(b)):
	c[k] = b[j]
	j+=1
	k+=1
print c
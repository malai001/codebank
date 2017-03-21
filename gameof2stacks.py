val = map(int,raw_input().split(' '))
a = map(int,raw_input().split(' '))
b = map(int,raw_input().split(' '))
s = 0
j = 0
i = 0
count = 0
while(i<val[0] and j<val[1]):
	if(a[i]<b[j]):
		s+=a[i]
		i+=1
		if(s<val[2]):
			count+=1
		else:
			break		
	else:
		s+=b[j]
		j+=1
		if(s<val[2]):
			count+=1
		else:
			break		
while (i<val[0]):
	s += a[i]
	i+=1
	if(s<val[2]):
		count+=1
	else:
		break
while(j<val[1]):
	s += b[j]
	j+=1
	if(s<val[2]):
		count+=1
	else:
		break

print count


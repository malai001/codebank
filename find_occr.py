a = [1, 2, 2, 2, 2, 3, 4, 7, 8, 8]
i = 0
j = len(a)-1
k = 8
curr = 0
curr1 = len(a)/2
while(i<=(len(a)/2) and j>(len(a)/2) ):
	if (a[i] == k):
		if(curr1 > i):
			curr1 = i	
	if(a[j] == k):
		if(curr<j):
			curr = j			
	i += 1
	j -= 1
	
if(curr1 == len(a)/2 and i == len(a)/2):
	if (curr != 0):
		curr1 = curr 
print curr1,
print curr
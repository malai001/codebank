n = input()
a = raw_input()
count = 0
val = 0
for i in range(0,n):
	if(a[i] == 'U'):
		count+=1
		if(count == 0):
			val +=1 	
	else:
		count-=1 
print val

a = [2,1,5,3,4]
count =0
for i in range(0,len(a)):
	if(abs(a[i]-a[i-1])<=2 and (abs(a[i+1]-a[i])<=2)): 
		count = count+1
	else:
		print ("Not Chaos")
		break
if(count <0):
	print ("Not Chaos")
elif(count > 0):
	print count
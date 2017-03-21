a = ["the","higher","you","climb","the","further","you","fall"]
b = []
for i in range(0,len(a)):
 	if(a.count(a[i])>1):
 		if a[i] not in b: 
 			b.append(a[i])
print len(b)
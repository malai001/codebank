l = [2,3,4]
l1 = [2,2,3,4,5]

def sublist(l1,l2):
 for i in range(len(l2)):
 	if(l1[0]==l2[i]):
 	for j in range(len(l1)):
 	if(l1[j]!=l2[i+j]):
 	break
 	elif(j==len(l1)-1):
 	return(True)
 return(False)
def book(k,i,a):
	if k not in a:
		a[i]=k
	else:
		print ("Seat Booked already")
def print_ticket(a):
	print (a)
def cancel_ticket(t,a):
	for i in range(0,len(a)-1):
		if(a[i]==t):
			del a[i] 
			print("ticket cancelled successfully and the ticket is",t)
def availablity(a):
	for i in range(0,6):
		if i not in a:
			print i	
def chart(a):
	print ("<-------------chart prepared------------->")
	for i in range(0,len(a)):
		if(a[i]!=0):
			print ("Customer-",i,"Seat No-",a[i])
a=[0]*5
book(2,0,a)
book(3,1,a)
#book(4,2,a)
#book(5,3,a)
#book(1,4,a)
book(2,0,a)
print_ticket(a)
#cancel_ticket(3,a)
#cancel_ticket(4,a)
#cancel_ticket(5,a)
#print_ticket(a)
chart(a)
availablity(a)
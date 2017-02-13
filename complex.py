p = 'A'
drop = 'B'
def amount(p,drop):
	dis = ord(drop)-ord(p) 
	dis = dis * 15 -5  
	amt = 100 + dis * 10
	return amt
a_dest = 0 
a_free = 0
b_free = 0
b_dest = 0
book_time = [9,9,10]
pick = ['a','b','b']
drop = ['b','c','c']
for i in range(0,len(pick)):
	if( a_free == 0 or a_free == book_time[i] or book_time[i] == ord(drop[i])-ord(pick[i])+a_free ):
		a_free = book_time[i]+(ord(drop[i])-ord(pick[i]))
		a_dest = drop[i]
		print ("Taxi - A is booked for you",a_free,a_dest)
		print ("The amount for you travel is ",amount(pick[i],drop[i]))
	elif( b_free == 0 or b_free == book_time[i] or book_time[i] == ord(drop[i])-ord(pick[i])+b_free ):
		b_free = book_time[i]+(ord(drop[i])-ord(pick[i]))
		b_dest = drop[i]
		print ("Taxi - B is booked for you ",b_free,b_dest)
		print ("The amount for you travel is ",amount(pick[i],drop[i]))
	else:
		print ("NO Taxi' are available right now,taxi's are available from")


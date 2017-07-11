a = input()
if(a>=1700 and a<=1917):
	if(a%4==0):
		print("12.09.%s"%a) 
	if(a%4!=0): 
		print("13.09.%s"%a) 
if(a==1918):
    print("26.09.1918");

if(a>1918 and a<=2700):
	if a%400 == 0:
		print '12.09.%s'%a
	elif a%4 == 0 and a%100 !=0 :
		print '12.09.%s'%a
	else:
		print '13.09.%s'%a

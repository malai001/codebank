a = [3,2,7,8,5]
def mystery(a):
		if a == []:
	   		return a
	   	else:
	   		return (a[-1:] + mystery(a[:-1]))

a = mystery(a)
print a
n = input()
a = raw_input()
l = input()
k = ''
if l>26:
	l = l%26
for i in a:
	m = ord(i)
	if (m >=65 and m<91): 
		v = m+l
		if v>90:
			v= v-26
		k+=chr(v)	
	elif (m>=97 and m<123): 
		v = m+l
		if v>122:
			v= v-26
		k+=chr(v)	
	else:
		k+= chr(m)
print k
import re
pattern = ">>REGISTER,<<401,>>REGISTER,<<200,>>REGISTER,<<200,>>REGISTER,<<200,>>REGISTER,>>REGISTER"
#msg = ">>REGISTER,<<401,>>REGISTER,<<200,>>REGISTER,<<200,>>REGISTER,<<200,>>REGISTER,>>REGISTER>>REGISTER"
#print pattern
msg = ('200', 2147000001, '>>REGISTER,<<401,>>REGISTER,<<200,>>REGISTER,<<200,>>REGISTER,<<200,>>REGISTER,>>REGISTER,>>REGISTER,<<200')
print msg[2]

if re.search(pattern ,msg[2]):
	print "passed"
else:
	print "failed"
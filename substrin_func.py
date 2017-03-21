msg = '>>REGISTER,<<401,>>REGISTER,<<200,>>REGISTER,<<200,>>REGISTER,<<200,>>REGISTER,>>REGISTER'
pattern = '>>REGISTER,<<200,>>REGISTER,>>REGISTER'
if pattern in msg:
	print ("passed")
else:
	print("failed")

 
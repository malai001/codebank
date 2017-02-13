import re
pattern = '''aabaa'''
msg = "aabbaa"
m =re.match(pattern,msg)
if m:
	print (m.group(0))
else:
	print (m.group(0),"***")


	
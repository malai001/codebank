import re

a = 'Cleanup: (200,st="ok",ref=29)'
b = '(200,id=1,ref=54)'

#refptn = re.compile()
refptn =  re.compile(r"""(.+),ref=(\d+).$""")

if refptn.match(b):
	Rec_ID = refptn.match(b).group(2)
	data   = refptn.match(b).group(1)+')'
print Rec_ID, data
# data = ''
# if 'ref=' in a:
# 	#Rec_ID = a.split(',')[-1].split('=')[-1].split(')')[0]
# 	#print Rec_ID

# 	k =  a.split(',')
# for i in xrange(len(k)-1):
# 	data+=k[i]+','
# data=str(data[:-1]+')')
# # data = str(data)
# print data
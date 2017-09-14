import os
a = os.listdir('C:\Program Files (x86)\GCTI\SIP Endpoint SDK')
val = 'TestSample-'
for i in a:
	if(val in i):
		os.chdir('C:\Program Files (x86)\GCTI\SIP Endpoint SDK')
		os.system('Rename %s TestSampleExe' % i )
		

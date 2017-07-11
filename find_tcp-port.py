import os
import sys

def netstats(base_port,key):
	c = 0
	d = {}
	lines = []
	while(c<key):
		val = base_port+c
		for line in os.popen('netstat -ano |find "%s"'%val):
			for i in line.split(' '):
				if i !='':
					lines.append(i)
		d[c] = lines
		lines = []
		c+=1
	v = []
	for i in d:
		if d[i][3]=='ESTABLISHED':
			pid = d[i][4]
			print pid
			for line in os.popen('tasklist /fi "pid eq %s""'%pid):
				if line.startswith('TestSampleVS2013.exe') or line.startswith("ecot.exe"):
					print line
					v.append(1)
	if len(v)==key:
		return 1				
print netstats(7060,2)
os.system('taskkill /F /T /IM ecot*')
os.system('taskkill /F /T /IM TestSampleVS2013*')

import json
total_time =[0]*(1)
v = {}

def val(x):
	total_time[0] +=x['duration']
	if x['state'] not in v:
		l = { str(x['state']): x['duration']} 
		v.update(l)
	else:
		v[x['state']] += x['duration']

with open('interview_json.json') as data:
	k = json.load(data)
	map(val,k)
	for i in v.keys():
		print float(v[i])/float(total_time[0])



# Previous Code
# for l in k:
# 	v[l['state']] = 0
# for i in k:
# 	x,total_time += i['duration']
# 	v[i['state']]+= i['duration']
# for l in v.keys():
#  	print float(v[l])/float(total_time)
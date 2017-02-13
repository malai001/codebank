def DFS(d,k,v):
	if k in v:
		return
	v.append(k)
	for e in [x for x in d[k] if x not in v]:
		DFS(d,e,v)
	return v		
d={}
i=[]
v=[] 

for y in range(0,4):
	d[y]=[int(x) for x in input()]
	print d[y] 
v=DFS(d,0,v)
print v
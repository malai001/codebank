cu,cd = map(int,raw_input().split())
a = map(int,raw_input().split(' '))
eff = cu-cd
count = 0
total = 0
for i in a:
	t=i/eff
	if((i-cu)%eff==0):
		t=(i-cu)/eff
	if((i%eff)>0):
		t+=1
	total+=t
print total

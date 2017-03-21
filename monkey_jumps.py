cu,cd = map(int,raw_input().split())
a = map(int,raw_input().split(' '))
eff = cu-cd
count = 0
total = 0
for i in range(0,len(a)):
	if(len(a) >=1):
		total += a[i]/eff
		if( a[i]%eff >=cu ):
			count += 1
		if((eff*(total-1) +cu == a[i])):
			total -=1
print total+count		
# goup,comedown=map(int,raw_input().split(' '))
# a=map(int,raw_input().split(' '))
# totaljump=0
# for i in a:
#     t=1
#     while(i-goup>0):
#         i=i-(goup-comedown)
#         t+=1
#     totaljump+=t
# print totaljump 
n,k = map(int,raw_input().split(' '))
#k = int(raw_input())
temp = n
s = 0
t = 240 - k
while(t > 0 ):
	if(temp > 0):
		s = s + 5
		t = t - s
		if(t>= s or t >= 0):
			temp = temp - 1
		
	if(temp == 0):
		break
print (n-temp)


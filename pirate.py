x = []
y = []
curr_x,curr_y = map(int,input()) 
n = input()
for i in range(0,n):
	x1,y1 = map(int,raw_input().split(','))
	x.append(x1)
	y.append(y1)
for i in x:
	if(i>0):
		curr_x = curr_x-i
	else:
		curr_x = curr_x+abs(i)
for i in y:
	if(i>0):
		curr_y = curr_y-i
	else:
		curr_y = curr_y+abs(i)
print curr_x,curr_y

1 2 3 4 5 6 7 8 9 10


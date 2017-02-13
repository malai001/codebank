# a = 21
# b = str(21)
# d=[]
# d.append(b)
# print(d[0][1:2])
def reverse(num):
  return int(str(num)[::-1])
i,j,k =map(int, raw_input().split())
#j = input()
#k=input()
count = 0 
for x in range(i,j):
	d=abs(x-reverse(x))
#print d
	r = d%k
	if (r == 0):
		count = count+1
print count		
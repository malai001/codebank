n = map(int,raw_input().split())
val = map(int,raw_input().split())
val.sort()

s = 0
count = 0
for i in val:
	if s+i <= n[1]:
		s+=i
		count+=1

print count
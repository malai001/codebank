

s = raw_input().strip()
d = []
d=s.split("(?=\\p{Upper})")
n= len(s)
print(d)
# for i in range(0,n):
#     if(int(d[i])<97):
#         count = count+1

# print(count+1)    
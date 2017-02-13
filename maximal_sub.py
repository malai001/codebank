a = [-3,2,1,2,1]
CONST_MAX = 10000
def get_max(a,b):
	res = a if a>b else b
	return res
def printPairs(arr, arr_size, sum):
     
    # initialize hash map as 0
    binmap = [0]*CONST_MAX
     
    for i in range(0,arr_size):
        temp = sum-arr[i]
        if (temp>=0 and binmap[temp]==1):
            print "Pair with the given sum is", arr[i], "and", temp
        binmap[arr[i]]=1
max1 = a[0]
glob = a[0]
for i in range(0,len(a)-1):
	max1 = get_max(a[i],a[i]+max1)
	if(max1>glob):
		glob = max1

printPairs(a, len(a) ,glob-2)
print glob
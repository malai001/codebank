a=[1,2,3,3,3,3,3,3,3,4,4]
l = 0
h= len(a)
x = 3
while(l <= h):
	mid = l+(h-l)/2
	print mid
	if(a[mid] == x and (x<a[mid+1]or mid == len(a)-1)):
		print('found at',mid)
		break
	if(a[mid]<x):
		l = mid+1
	else:
		h = mid-1

# if( ( mid == 0 || x > arr[mid-1]) && arr[mid] == x)
#             return mid;
#         else if(x > arr[mid])
#             return first(arr, (mid + 1), high, x, n);
#         else
#             return first(arr, low, (mid -1), x, n);
#        if (( mid == n-1 || x < arr[mid+1]) && arr[mid] == x)

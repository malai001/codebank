import sys

def isSatisfiable(c1, c2, h1, h2):
    # Complete this function
    if c1>=35 and c2>=35 and c1<=h1 and c1<=h2 and c2<=h1 and c2 <=h2 :
    	if h1 <=95 and h2 <=95:
    		return 'Yes'
    	else:
    		return 'No'
    else:
    	return 'No'	

# Return "YES" if all four conditions can be satisfied, and "NO" otherwise
c1, c2, h1, h2 = raw_input().strip().split(' ')
c1, c2, h1, h2 = [int(c1), int(c2), int(h1), int(h2)]
result = isSatisfiable(c1, c2, h1, h2)
print(result)
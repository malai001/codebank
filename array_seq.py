# Enter your code here. Read input from STDIN. Print output to STDOUT
n,t = map(int,raw_input().split())
headers = [[] for i in range(0,n)]
for i in range(0,t):
    las_ans=0
    q,t,h = map(int,raw_input().split())
    if(q==1):
        val = ((t^las_ans)%2)
        headers[val].append(h)
        print headers[val]
    elif(q==2):
        val = ((t^las_ans)%2)
        size = len(headers[val])
        temp=[]
     	temp = headers[val]
        #print (headers[val])
        las_ans= temp[h%size]
        print las_ans
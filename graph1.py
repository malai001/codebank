g={}
def dsf(lis):
    for i in lis:
        if l_v[i]==0:
            print "going to node ",i
            l_v[i]=1
            dsf(g.get(i))

for i in xrange(int(raw_input('Enter the no of nodes: '))):
    print "Enter the vertices of "+str(i)+" as space seprated: "
    val=map(int,raw_input().strip().split(' '))
    g[i]=val
l_v={}
print g
for i in g.keys():
    l_v[i]=0
print "Starting from the node 0"
l_v[0]=1
dsf(g.get(0)) 
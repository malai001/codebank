import operator
def func(a):
	d = {}
	final_a = []
	final_b = []
	a_l_l = []
	b_l_l = []
	final_b.append(0)
	final_b.append(0)
	final_a.append(0)
	final_a.append(0)
	a_l,b_l,m_l = a.split(':')
	m_l = m_l.split(',')
	tot_val = 0
	tot_val1 = 0
	count = 0
	count1 =0
	for i in m_l:
		val=i.split('-')[0]
		val1=i.split('-')[1]
		tot_val += int(val)
		tot_val1+= int(val1)
		if(val>val1):
			a_l_l.append(val)
		else:
			b_l_l.append(val1)
	if(len(m_l) <= 5 and len(m_l) >3 ):
	 	count = final_a[0]
	 	count += 1
	 	final_a[0] = count
	else:
		count = final_a[0]
		final_a[0] = count
	if(len(m_l) <= 3 ):
	 	count = final_a[1]
	 	count += 1
	 	final_a[1] = count
	else:
		count = final_a[1]
		final_a[1] = count
	final_a.append(len(a_l_l))
	final_b.append(len(b_l_l))
	final_b.append(tot_val1)
	final_a.append(tot_val)
	final_a.append(len(b_l_l))
	final_b.append(len(a_l_l))
	final_a.append(tot_val1)
	final_b.append(tot_val)

	d[a_l] = final_a
	d[b_l] =  final_b
	return d
	
def final_dict(d,b):
	for i in d.keys():
		if i not in b:
			b[i] = d[i]
			#print b
		else:
			a = b[i]
			c = d[i]
			a[0] += c[0]
			a[1] += c[1]
			a[2] += c[2]
			a[3] += c[3]
			a[4] += c[4]
			a[5] += c[5]
			b[i] =a
	return b

def sort_dict(b):
  output = reversed(sorted(b.items(), key=operator.itemgetter(1)))
  print("\n".join([(i[0] + " "+" ".join([str(j) for j in i[1]])) for i in output]))

b ={}
base = []
line=input()
while(len(line)>1):
  base.append(line)
  line=input()
for i in base:
 	d = func(i)
 	b = final_dict(d,b)
sort_dict(b)
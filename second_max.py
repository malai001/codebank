def secondmax(l):
  (mymax,mysecondmax) = (0,0)
  for i in range(len(l)):
  # Your code below this line
  	l.sort()
  	mysecondmax = l[len(l)-2]

  # Your code above this line
  return(mysecondmax)
l = [4,1,5]
print secondmax(l)  
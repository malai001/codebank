def f(x):
  d=0
  while x > 1:
    (d,x) = (d+1,x/10)
  return(d)
print(f(1782818))  
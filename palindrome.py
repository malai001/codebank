l = [13,14,13,14]
def mypalindrome(l):
  if l==[] or len(l) == 1:
    return(True)
  else:

    return(l[0]==l[-1] and mypalindrome(l[1:-1]))
print l[1:-1]
print l[1:-1]

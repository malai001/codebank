import operator
a = {'znna': [ 2,0,3],'malai': [1,3,3] }

print operator.itemgetter(2)
print sorted(a.items(),key = operator.itemgetter(0))
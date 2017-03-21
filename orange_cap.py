def orangecap(d):
  total = {}
  for k in d.keys():
    for n in d[k].keys():
      if n in total.keys():
        total[n] = total[n] + d[k][n]
      else:
        total[n] = d[k][n]

  maxtotal = -1
  for n in total.keys():
    if total[n] > maxtotal:
      maxname = n
      maxtotal = total[n]

  return(maxname,maxtotal)

d = {'match1':{'player1':57, 'player2':38}, 'match2':{'player3':9, 'player1':42}, 'match3':{'player2':41, 'player4':63, 'player3':91}}
print orangecap(d)
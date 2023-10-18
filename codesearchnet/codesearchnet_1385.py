def printOverlaps(comparedTo, coincs, seen):
  """ Compare the results and return True if success, False if failure
    
  Parameters:
  --------------------------------------------------------------------
  coincs:               Which cells are we comparing?
  comparedTo:           The set of 40 cells we being compared to (they have no overlap with seen)
  seen:                 Which of the cells we are comparing to have already been encountered.
                        This helps glue together the unique and reused coincs
  """
  inputOverlap = 0
  cellOverlap = 0
  for y in comparedTo:
    closestInputs = []
    closestCells = []
    if len(seen)>0:
      inputOverlap = max([len(seen[m][1].intersection(y[4])) for m in xrange(len(seen))])
      cellOverlap = max([len(seen[m][0].intersection(y[1])) for m in xrange(len(seen))])
      for m in xrange( len(seen) ):
        if len(seen[m][1].intersection(y[4]))==inputOverlap:
          closestInputs.append(seen[m][2])
        if len(seen[m][0].intersection(y[1]))==cellOverlap:
          closestCells.append(seen[m][2])
    seen.append((y[1], y[4], y[0]))
        
    print 'Pattern',y[0]+1,':',' '.join(str(len(z[1].intersection(y[1]))).rjust(2) for z in coincs),'input overlap:', inputOverlap, ';', len(closestInputs), 'closest encodings:',','.join(str(m+1) for m in closestInputs).ljust(15), \
    'cell overlap:', cellOverlap, ';', len(closestCells), 'closest set(s):',','.join(str(m+1) for m in closestCells)
  
  return seen